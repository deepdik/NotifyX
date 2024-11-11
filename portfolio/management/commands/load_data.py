# portfolio/management/commands/load_initial_data.py

from django.core.management.base import BaseCommand
from portfolio.models import CollegeItem, ProjectItem, BlogItem, WorkExperience, Chip, WorkExperienceTask



class Command(BaseCommand):
    help = 'Load initial data into the database'

    def handle(self, *args, **options):
        # Clear existing data (optional)
        # Uncomment the following lines if you want to reset the data each time
        # CollegeItem.objects.all().delete()
        # ProjectItem.objects.all().delete()
        # BlogItem.objects.all().delete()
        # WorkExperience.objects.all().delete()
        # Chip.objects.all().delete()

        # 1. College Items Data
        college_items_data = [
            {'id': 1, 'college': 'Illinois Institute of Technology, Chicago, IL', 'major': 'Master of Computer Science', 'year': 'May 2025'},
            {'id': 2, 'college': 'Dr. A. P. J. Abdul Kalam Technical University, Lucknow, India', 'major': 'Bachelor of Technology', 'year': 'Jun 2018'},
        ]

        # 2. Project Items Data
        project_items_data = [
            {
                'id': 1,
                'title': 'Payment Service (TrueRev)',
                'banner_image': 'payment.svg',  # Update with actual image paths if available
                'description': (
                    "Engineered and implemented a high-performance payment microservice for a SaaS platform, integrating Stripe (Payment Gateway) with advanced security and payment distribution features. "
                    "Leveraged 3D Secure authentication to enhance transaction security and customer trust, while incorporating split payment functionality to optimize revenue allocation among multiple stakeholders. "
                    "This strategic development resulted in a 10% reduction in payment processing costs, significantly improving the platform's financial efficiency and user experience."
                ),
                'chips': ['Back-End Web Development', 'Python', 'Django', 'RabbitMQ', 'Firebase', 'MySQL', 'Distributed Systems', 'Stripe', 'Kafka', 'Micro Services'],
            },
            {
                'id': 2,
                'title': 'Automation Multipurpose Platform (Marc)',
                'banner_image': 'marc.svg',
                'description': (
                    "Played a pivotal role in the development of a highly adaptable automation health and analytics platform. "
                    "Efficiently managed and optimized over 10k+ engine configuration files, leading to precise assessments of system effectiveness and the identification of critical areas for enhancement by using Machine learning. "
                    "Engineered an advanced URL resolution system for robust authorization by implementing a Trie data structure, significantly improving performance and security. "
                    "Spearheaded the design and development of both the API gateway service and the authentication service. "
                    "Resulting reduced manual effort by 80% in identifying and compiling monthly progress reports. Extracted data from logs database and generating trigger emails for critical issues, ensuring timely alerts and responses."
                ),
                'chips': ['Micro Services', 'React', 'Java', 'Python', 'Flask', 'SpringBoot', 'Redis', 'MySQL', 'OracleDB', 'Docker', 'Kubernetes', 'Distributed Systems'],
            },
            {
                'id': 3,
                'title': 'E-commerce Site (IfashionUp)',
                'banner_image': 'ecom.svg',
                'description': (
                    "Collaborated to build an e-commerce platform built on a scalable E-commerce platform on a microservices architecture distributed system, ensuring high scalability and availability. "
                    "This comprehensive effort resulted in a 40% surge in online sales within the first quarter post-launch. "
                    "The platform's improved design, functionality, and user experience played a crucial role in this success. "
                    'The impact of this achievement was recognized with the prestigious "Code of the Month" award, highlighting the exceptional quality and effectiveness of the solution.'
                ),
                'chips': ['Micro Services', 'Python', 'Django', 'Firebase', 'MySQL', 'MongoDB', 'Redis', 'EC2', 'S3', 'AWS', 'Docker', 'Stripe', 'Kafka', 'Elastic Search'],
            },
            {
                'id': 4,
                'title': 'Laboratory Management (GenistaBio)',
                'banner_image': 'lab.svg',
                'description': (
                    "Contributed to the Laboratory Management software by developing robust backend APIs for seamless integration with frontend functionality. "
                    "Users upload samples collected by customers in PDF and XLS files, which are read to identify all samples and the rules that need to be applied. "
                    "The backend then resolves all required tests for each sample, generates comprehensive reports, and sends them to users. "
                    "The system features robust authentication with role-based permissions, ensuring secure access and management. "
                    "These improvements reduced sample processing time by 37%, leading to a 16% increase in monthly revenue."
                ),
                'chips': ['Back-End Web Development', 'Python', 'Django', 'RabbitMQ', 'MySQL', 'Test Driven Development', 'Distributed Systems'],
            },
            {
                'id': 5,
                'title': 'Social Media (Viewed)',
                'banner_image': 'viewed.svg',
                'description': (
                    "Built a highly engaging social media platform with an Instagram-like feed featuring posts in image, text, and video formats. "
                    "Users can create unique lucky draw posts where multiple participants join and a random winner is selected. "
                    "The platform allows users to follow an unlimited number of other users and offers extensive settings options for customization. "
                    "Developed on top of a microservices event-driven architecture, the platform achieved rapid scalability and high performance. "
                    "Within one month of launch, the platform attracted over 10k users and facilitated over 30k posts, demonstrating its widespread popularity and robust functionality."
                ),
                'chips': ['Back-End Web Development', 'Python', 'Django', 'RabbitMQ', 'Firebase', 'MySQL', 'PostgreSQL', 'Test Driven Development', 'Distributed Systems'],
            },
            {
                'id': 6,
                'title': 'Project Management Software (FinoitPMS)',
                'banner_image': 'finpms-2.svg',
                'description': (
                    "Developed an integrated, scalable platform on a microservices distributed architecture to manage employee attendance, efficiency, project health, invoices, revenue distribution, and security. "
                    "Initially built for internal use, the platform's success led to its commercialization, contributing to 25% of the company's total revenue. "
                    "The platform improved project health with a 15% reduction in project delays and an 18% increase in on-time completions. "
                    "This highly successful project demonstrated significant positive impacts on both internal operations and the company's financial performance."
                ),
                'chips': ['Back-End Web Development', 'Python', 'Django', 'PostgreSQL', 'Docker', 'AWS SQS', 'LDAP', 'Distributed Systems', 'Micro Services'],
            },
        ]

        # 3. Blog Items Data
        blog_items_data = [
            {
                'id': 1,
                'title': 'Zero Downtime Schema Changes in Microservices: A Real-World Guide',
                'banner_image': 'llm.svg',
                'description': (
                    "In today’s fast-paced software world, businesses can’t afford downtime. "
                    "Whether you’re running a global e-commerce platform or a SaaS product for millions of users, even a few minutes of downtime can result in lost revenue, frustrated users, and potentially damaged reputations."
                ),
                'chips': ['Back-End Web Development', 'Apache Kafka', 'Python', 'MongoDB', 'Redis', 'Test Driven Development', 'Distributed Systems'],
                'redirect': 'http://localhost:3000/sedfe/ewded/dwde',
            },
            {
                'id': 2,
                'title': 'Neural Networks behind the Chat-GPT',
                'banner_image': 'Neural_Networks_Chat_gpt.svg',
                'description': (
                    "The neural network in ChatGPT is a type of machine learning model that relies on small mathematical functions called neurons. "
                    "These neurons work together to process and understand complex patterns in the input data, enabling ChatGPT to generate coherent and contextually relevant text."
                ),
                'chips': ['Tag C', 'Tag D'],
                'redirect': 'http://localhost:3000/wdhd/wdewd/ewded',
            },
            {
                'id': 3,
                'title': 'Building a NLP model like Transformer from scratch',
                'banner_image': 'nlp.svg',
                'description': (
                    "The transformer architecture comprises an encoder-decoder structure. "
                    "The encoder processes input sequences, and the decoder generates output sequences. "
                    "Key components include self-attention mechanisms, feedforward networks, and layer normalization. "
                    "A crucial innovation in transformers is the self-attention mechanism. It allows the model to weigh different parts of the input sequence differently, enabling effective handling of long-range dependencies."
                ),
                'chips': ['Back-End Web Development', 'Apache Kafka', 'Python', 'MongoDB', 'Redis', 'Test Driven Development', 'Distributed Systems'],
                'redirect': 'http://localhost:3000/wne/efef/efef',
            },
            {
                'id': 4,
                'title': 'Large Scale Distributed Models and its deployment',
                'banner_image': 'large_scale_model1.svg',
                'description': (
                    "Scaling and deploying large-scale distributed machine learning (ML) models efficiently involves several best practices:"
                ),
                'chips': ['Back-End Web Development', 'Apache Kafka', 'Python', 'MongoDB', 'Redis', 'Test Driven Development', 'Distributed Systems'],
                'redirect': 'http://localhost:3000/sd/edf/edfdef',
            },
            {
                'id': 5,
                'title': 'All about Large Language Models',
                'banner_image': 'llm.svg',
                'description': (
                    "Large Language Models (LLMs) are a revolutionary development in artificial intelligence, particularly in the field of natural language processing. Here's a concise overview."
                ),
                'chips': ['Back-End Web Development', 'Apache Kafka', 'Python', 'MongoDB', 'Redis', 'Test Driven Development', 'Distributed Systems'],
                'redirect': 'http://localhost:3000/sedfe/ewded/dwde',
            },
            {
                'id': 6,
                'title': 'All about Large Language Models',
                'banner_image': 'llm.svg',
                'description': (
                    "Large Language Models (LLMs) are a revolutionary development in artificial intelligence, particularly in the field of natural language processing. Here's a concise overview."
                ),
                'chips': ['Back-End Web Development', 'Apache Kafka', 'Python', 'MongoDB', 'Redis', 'Test Driven Development', 'Distributed Systems'],
                'redirect': 'http://localhost:3000/sedfe/ewded/dwde',
            },
        ]

        # 4. Work Experience Items Data
        work_experience_items_data = [
            {
                'id': 1,
                'title': 'Software Engineer',
                'company': 'Oracle',
                'skills': [
                    'Back-End', 'Front-End', 'Python', 'Spring Boot', 'Java', 'Flask', 'FastAPI', 'Redis', 'Spring Cloud',
                    'Hibernate', 'JDBC', 'SQLAlchemy', 'Event Driven Architecture', 'Distributed Systems', 'Event-driven',
                    'Docker', 'Kubernetes', 'Jenkins', 'React', 'OracleDB', 'MySQL', 'HTML', 'CSS', 'Javascript'
                ],
                'start_date': 'MAY-2021',
                'end_date': 'AUG-2023',
                'tasks': [
                    'Developed Python graph algorithm to identify invalid objects in Oracle Databases. Achieved a remarkable 50% reduction in time to resolve customer service requests.',
                    'Enhanced functionality through cross-team collaboration, successfully troubleshooting and resolving over 10+ bugs, and seamlessly integrating 5+ new features into core automation engine.',
                    'Created Python script using graph algorithm to automate XML output validation from core automation engine, cutting manual testing effort by 100%.',
                    'Built survey platform on microservices architecture for Database RCA Analysis, slashing analysis time by 75%. Helped to analyze customer trace file upload behavior towards different severity issues.',
                    'Contributed to developing a versatile automation health and analytics platform. Helped to manage 10k+ core engine config files, assess system effectiveness, and pinpointing areas for improvement. Leveraged Java, Python, Hibernate, Spring Cloud, Docker, and Kubernetes to architect.',
                ],
            },
            {
                'id': 2,
                'title': 'Software Engineer',
                'company': 'Finoit Technologies',
                'skills': [
                    'Back-End', 'Python', 'Django', 'AWS', 'S3', 'EC2', 'SES', 'AWS-Lambda', 'Stripe', 'Payment-Gateway',
                    'Redis', 'Test Driven Development', 'Distributed Systems', 'Docker', 'CI/CD', 'Kafka', 'Selenium', 'Memcached'
                ],
                'start_date': 'JAN-2020',
                'end_date': 'APR-2021',
                'tasks': [
                    'Designed and developed payment microservice for SaaS Platform, integrating Stripe with 3D Secure and split payment functionality, resulting in a 10% reduction in payment processing costs.',
                    'Developed an integrated platform to manage employee attendance, efficiency of employees, health of projects, invoices, revenue distribution, and security. Project health improved, with a 15% reduction in project delays and an 18% increase in on-time completions.',
                    'Contributed to Laboratory Management software, developing robust backend APIs for seamless integration with frontend functionality, reducing sample process time by 37% and yielding a 16% increase in monthly revenue.',
                    'Provided guidance and mentorship to junior colleagues, nurturing their professional growth and development.'
                ],
            },
            {
                'id': 3,
                'title': 'Software Engineer',
                'company': 'Fluper Ltd',
                'skills': [
                    'Back-End', 'Front-End', 'Python', 'Django', 'MySQL', 'PostgreSQL', 'ORM', 'Twilio', 'Celery', 'RabbitMQ',
                    'Angular', 'HTML', 'CSS', 'Javascript', 'jQuery', 'MongoDB', 'Caching'
                ],
                'start_date': 'FEB-2019',
                'end_date': 'JAN-2020',
                'tasks': [
                    'Enhanced existing API performance by 300% by using async task management with RabbitMQ and Celery. Used caching mechanisms to reduce redundant computations and database queries.',
                    'Led and orchestrated end-to-end development for a client\'s e-commerce platform, resulting in a 40% surge in online sales within the initial quarter post-launch.'
                ],
            },
            {
                'id': 4,
                'title': 'Software Engineer Intern',
                'company': 'BrandsBrother',
                'skills': ['Full Stack Web Development', 'Django', 'Python', 'MySQL', 'ORM'],
                'start_date': 'OCT-2018',
                'end_date': 'JAN-2019',
                'tasks': [
                    'Developed RESTful APIs for TouristShop portal, facilitating effortless online booking of travel packages, resulting in an 8% increase in bookings.',
                    'Integrated third-party APIs to extend portal functionality and features.'
                ],
            },
        ]

        # Collect all unique chips/skills
        all_chip_names = set()
        for item in project_items_data:
            all_chip_names.update(item['chips'])
        for item in blog_items_data:
            all_chip_names.update(item['chips'])
        for item in work_experience_items_data:
            all_chip_names.update(item['skills'])

        # Create or get Chip instances
        chip_objects = {}
        for name in all_chip_names:
            chip, created = Chip.objects.get_or_create(name=name)
            chip_objects[name] = chip
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Chip: {chip.name}'))
            else:
                self.stdout.write(f'Existing Chip: {chip.name}')

        # Insert College Items
        for item in college_items_data:
            college_item, created = CollegeItem.objects.get_or_create(
                college=item['college'],
                major=item['major'],
                year=item['year'],
                order=item['id']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created CollegeItem: {college_item}'))
            else:
                self.stdout.write(f'Existing CollegeItem: {college_item}')

        # Insert Project Items
        for item in project_items_data:
            project_item, created = ProjectItem.objects.get_or_create(
                title=item['title'],
                description=item['description'],
                order=item['id']
            )
            # Assign chips
            chips = [chip_objects[name] for name in item['chips'] if name in chip_objects]
            project_item.chips.set(chips)
            project_item.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created ProjectItem: {project_item}'))
            else:
                self.stdout.write(f'Existing ProjectItem: {project_item}')

        # Insert Blog Items
        for item in blog_items_data:
            blog_item, created = BlogItem.objects.get_or_create(
                title=item['title'],
                description=item['description'],
                redirect=item['redirect'],
                order=item['id']
            )
            # Assign chips
            chips = [chip_objects[name] for name in item['chips'] if name in chip_objects]
            blog_item.chips.set(chips)
            blog_item.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created BlogItem: {blog_item}'))
            else:
                self.stdout.write(f'Existing BlogItem: {blog_item}')

        # Insert Work Experience Items
        for item in work_experience_items_data:
            work_exp, created = WorkExperience.objects.get_or_create(
                title=item['title'],
                company=item['company'],
                start_date=item['start_date'],
                end_date=item['end_date'],
                order=item['id']
            )
            # Assign skills
            skills = [chip_objects[name] for name in item['skills'] if name in chip_objects]
            work_exp.skills.set(skills)
            work_exp.save()

            # Create WorkExperienceTask instances
            for task_description in item['tasks']:
                task, task_created = WorkExperienceTask.objects.get_or_create(
                    work_experience=work_exp,
                    description=task_description
                )
                if task_created:
                    self.stdout.write(self.style.SUCCESS(f'Created Task for {work_exp}: {task_description[:50]}'))
                else:
                    self.stdout.write(f'Existing Task for {work_exp}: {task_description[:50]}')

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created WorkExperience: {work_exp}'))
            else:
                self.stdout.write(f'Existing WorkExperience: {work_exp}')

        self.stdout.write(self.style.SUCCESS('Data loading completed successfully.'))

        self.stdout.write(self.style.SUCCESS('Data loading completed successfully.'))
