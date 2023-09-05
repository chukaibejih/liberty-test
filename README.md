# BACKEND APPLICATION -TEST - LIBERTY ASSURED (Blog Application)

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

This Django Rest Framework blog application was developed as part of a test to demonstrate proficiency in designing and developing backend systems. It includes features for creating and editing blog posts, user authentication, sharing blogs with other authors, filtering and sorting blogs, and listing authors with access to each blog.

## Requirements

To run this application, you need the following:

- Language: Python 3.10
- Framework: Django 4.0+
- Database: PostgreSQL
- Testing: Django Test Framework
- Test Coverage: 80%+
- Development Methodology: TDD (Test Driven Development)
- Other dependencies as specified in the `requirements.txt` file.

## Features

1. **Blog and Author Models:** Django models for storing blog and author information.
2. **Authentication:** Secure authentication system to protect the application's functionality.
3. **Edit Blog Post:** Authors can edit their own blog posts.
4. **Edit Author Details:** Authors can update their personal information.
5. **Sharing of Blogs:** Authors can share their blogs with other authors, granting access to edit and manage content.
6. **Share Blog View:** A view displays shared blogs, making it easy for authors to access and collaborate on shared content.
7. **Blog Filter View:** A filter view allows users to search and sort blogs by various criteria.
8. **List of Authors with Access:** Displays a list of authors who have access to each blog.
9. **Class-Based Views:** Utilizes class-based views for consistency.

## Getting Started

Getting Started
---------------

To run the API locally, follow these steps:

1.  Clone the repository
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the virtual environment: `source venv/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Change `.env.templates` to .env and setup you environment variables. 
6.  Set up the database: `python manage.py migrate`
7.  Start the development server: `python manage.py runserver`


Running Tests
---------------

To run all the tests, use the following command:

    ```
    python manage.py test
    ```

Authentication
--------------

Authentication is required for most endpoints in the API. To authenticate, include an access token in the `Authorization` header of your request. The access token can be obtained by logging in to your account or registering a new account.

Limitations
------------

While the application has been designed to meet various requirements, it also has some limitations:

- No Configured Email Backend: Currently, the application does not have a configured email backend. As a result, registered users are verified by default, instead of receiving an email for verification.
- I left DEBUG=True due to collectstatic issues with render(Cloud service)

## API Endpoints

### Account App

#### User Registration

- **Endpoint:** `/register/`
- **Description:** Allows users to register with the application.
- **HTTP Method:** POST
- **Authentication:** Not required
- **View:** `RegistrationView`

#### User Login

- **Endpoint:** `/login/`
- **Description:** Allows users to log in and obtain an authentication token.
- **HTTP Method:** POST
- **Authentication:** Not required
- **View:** `CustomTokenObtainPairViewSet`

#### Token Refresh

- **Endpoint:** `/token/refresh/`
- **Description:** Allows users to refresh their authentication token.
- **HTTP Method:** POST
- **Authentication:** Required (valid token)
- **View:** `TokenRefreshView`

#### Email Confirmation

- **Endpoint:** `/confirm_email/<str:uidb64>/<str:token>/`
- **Description:** Allows users to confirm their email address.
- **HTTP Method:** GET
- **Authentication:** Not required
- **View:** `ConfirmEmailView`

#### Change Password

- **Endpoint:** `/change_password/`
- **Description:** Allows users to change their password.
- **HTTP Method:** POST
- **Authentication:** Required (valid token)
- **View:** `ChangePasswordView`

#### Password Reset

- **Endpoint:** `/password_reset/`
- **Description:** Provides password reset functionality. (Uses `django_rest_passwordreset` library)
- **HTTP Method:** POST
- **Authentication:** Not required
- **View:** `password_reset` (provided by `django_rest_passwordreset`)

#### User List

- **Endpoint:** `/users/`
- **Description:** Retrieves a list of users.
- **HTTP Method:** GET
- **Authentication:** Required (valid token)
- **View:** `UserListView`

#### User Detail

- **Endpoint:** `/users/<str:pk>/`
- **Description:** Retrieves details of a specific user.
- **HTTP Method:** GET
- **Authentication:** Required (valid token)
- **View:** `UserDetailView`

#### User Profile Retrieve/Update

- **Endpoint:** `/user-profile/<str:pk>/`
- **Description:** Allows users to retrieve and update their profiles.
- **HTTP Methods:** GET (retrieve), PUT/PATCH (update)
- **Authentication:** Required (valid token)
- **View:** `UserProfileRetrieveUpdateView`

### Blog App

#### Blog List/Create

- **Endpoint:** `/`
- **Description:** Lists existing blogs and allows authors to create new ones.
- **HTTP Methods:** GET (list), POST (create)
- **Authentication:** Required (valid token)
- **View:** `BlogViewset`

#### Blog Detail/Update/Delete

- **Endpoint:** `/blogs/<str:pk>/`
- **Description:** Retrieves, updates, or deletes a specific blog.
- **HTTP Methods:** GET (retrieve), PUT/PATCH (update), DELETE (delete)
- **Authentication:** Required (valid token)
- **View:** `BlogViewset`

#### Share Blog

- **Endpoint:** `/share/`
- **Description:** Allows authors to share their blogs with other authors.
- **HTTP Method:** POST
- **Authentication:** Required (valid token)
- **View:** `BlogSharingView`

#### Shared Blogs List

- **Endpoint:** `/shared-blogs/`
- **Description:** Lists blogs that have been shared with the authenticated author.
- **HTTP Method:** GET
- **Authentication:** Required (valid token)
- **View:** `SharedBlogsListView`

#### Authors with Access

- **Endpoint:** `/authors-with-access/`
- **Description:** Lists authors who have access to blogs shared by the authenticated author.
- **HTTP Method:** GET
- **Authentication:** Required (valid token)
- **View:** `AuthorsWithAccessView`

