import random
import string
from django.contrib.auth.models import Group
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory

from main.models import BoardUser, Company, Category, Job
from main.views import job_post, jobs


class BoardUserTestCase(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name='company_name')
        cv_file = SimpleUploadedFile('cv.csv', content=b'', content_type='text/csv')
        user_photo = SimpleUploadedFile('photo.png', content=b'', content_type='image/png')
        self.employer = BoardUser.objects.create(
            username='employer',
            first_name='tony',
            last_name='montana',
            email='employer@gmail.com',
            password='password',
            is_active=True,
            company=self.company
        )
        self.jobseeker = BoardUser.objects.create(
            username='jobseeker',
            first_name='jacob',
            last_name='montana',
            email='jobseeker@gmail.com',
            password='password',
            is_active=True,
            cv_file=cv_file,
            user_photo=user_photo
        )
        self.category = Category.objects.create(name='Design & Creative')
        self.group_employer = Group.objects.create(name='employer')
        self.group_jobseeker = Group.objects.create(name='jobseeker')
        self.employer.groups.add(self.group_employer)
        self.jobseeker.groups.add(self.group_jobseeker)

    def test_groups_instances(self):
        """
        check if created users in groups
        """
        self.assertQuerysetEqual(self.employer.groups.all(), [self.group_employer])
        self.assertQuerysetEqual(self.jobseeker.groups.all(), [self.group_jobseeker])

    def test_job_post_view(self):
        """
        check if a user could post a job depending on the permissions
        """
        factory = RequestFactory()
        data = {'name': ['Software Engineer'],
                'category': ['2'], 'description': ['Software Engineer'],
                'responsibility': ['Software Engineer'], 'qualifications': ['Software Engineer'],
                'benefits': ['Software Engineer'], 'positions_number': ['1'], 'salary_from': [''],
                'salary_to': [''], 'location': ['Belarus'], 'job_nature': ['Full-time']}
        request = factory.post('job_post', data)

        # ignore messages from view
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        request.user = self.employer  # user is employer
        response = job_post(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.employer.created_by.all()[0], Job.objects.all())  # the job was successfully added

        request.user = self.jobseeker  # user is jobseeker
        response = job_post(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')  # redirect to index with message

        self.employer.company = None
        request.user = self.employer  # user is employer without company
        response = job_post(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/settings/')  # redirect to settings with message
        self.employer.company = self.company


class SearchTestCase(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name='Google')
        self.employer = BoardUser.objects.create(
            username='employer',
            first_name='tony',
            last_name='montana',
            email='employer@gmail.com',
            password='password',
            is_active=True,
            company=self.company
        )
        category1 = Category.objects.create(name='Software & Web')
        category2 = Category.objects.create(name='Marketing')
        Job.objects.create(
            name='Software Engineer',
            category=category1,
            description='Some description',
            responsibility='Some responsibilities',
            qualifications='Some qualifications',
            benefits='Some benefits',
            location='Belarus',
            job_nature='Full-time',
            created_by=self.employer)
        Job.objects.create(
            name='Marketer',
            category=category2,
            description='Some description',
            responsibility='Some responsibilities',
            qualifications='Some qualifications',
            benefits='Some benefits',
            location='USA',
            job_nature='Part-time',
            created_by=self.employer)
        self.group_employer = Group.objects.create(name='employer')
        self.employer.groups.add(self.group_employer)

    @staticmethod
    def get_random_string():
        return ''.join(random.choice(string.printable) for i in range(random.randint(0, len(string.printable))))

    def test_jobs_search_view(self):
        """
        input random values
        """
        factory = RequestFactory()
        for i in range(100):
            data = {'q': [self.get_random_string()], 'company': [self.get_random_string()],
                    'location': [self.get_random_string()], 'category': [self.get_random_string()],
                    'job_nature': [self.get_random_string()], 'undefined': [self.get_random_string()]}
            request = factory.get('jobs', data)

            # ignore messages from view
            setattr(request, 'session', 'session')
            messages = FallbackStorage(request)
            setattr(request, '_messages', messages)

            response = jobs(request)
            self.assertEqual(response.status_code, 200)
