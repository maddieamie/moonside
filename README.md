Moonside API Reflection App
===========================

Maddie Amelia Lewis
-------------------

### Description

For those interested in connecting their personal reflections or moods to the lunar cycle, finding both moon phase data and a place to record insights is cumbersome. This app simplifies the process by combining both functionalities in one location. Users can track their entries based on the moon's cycle over time, all within an intuitive and personalized interface.

### Features

-   **Personalized User Profiles**: Each user can create an account, update their profile, and set a unique profile picture linked to moon phases.
-   **Moon Phase Tracking**: The app pulls real-time moon phase data from an external API, allowing users to view the current phase and track its changes.
-   **Journal Entries**: Users can log personal reflections, moods, or events tied to a specific moon phase and review past entries.
-   **Dynamic Calendar**: View moon phases for an entire month and navigate through past entries.
-   **Automatic Moon Phase Data Fetching**: Moon phase data is fetched periodically to ensure it is always up to date for users.

### Technologies Used

-   **Django**: Backend framework for creating APIs and managing user data.
-   **PostgreSQL**: Database for storing moon phase data, user journal entries, and profiles.
-   **Tailwind CSS**: For styling the frontend in a responsive and modern design.
-   **Huey**: Task queue for scheduling periodic tasks, like fetching new moon phase data.
-   **Redis**: Cache system to handle session storage and task management efficiently.
-   **External API Integration**: Fetch moon phase data from `api.weatherapi.com`.
-   **Django Rest Framework**: For building the API endpoints.

### Installation

#### Requirements

-   Python 3.8+
-   Django 5.1.2
-   PostgreSQL 14
-   Redis
-   Huey

#### Setup to run locally

1.  **Clone the Repository:**

    bash

    Copy code

    `git clone https://github.com/your-username/moonside-api-reflection-app.git
    cd moonside-api-reflection-app`

2.  **Create a Virtual Environment and Install Dependencies:**

    bash

    Copy code

    `python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt`

3.  **Set Up Environment Variables:** Create a `.env` file at the root of the project and add the following variables:

    plaintext

    Copy code

    `PGDATABASE=your_database_name
    PGUSER=your_postgres_user
    PGPASSWORD=your_postgres_password
    PGHOST=localhost
    PGPORT=5432
    REDIS_PRIVATE_URL=redis://localhost:6379/0
    WEATHER_API_KEY=your_weather_api_key`

4.  **Create and Apply Migrations:**

    bash

    Copy code

    `python manage.py migrate`

5.  **Create a Superuser to Access the Admin Panel:**

    bash

    Copy code

    `python manage.py createsuperuser`

6.  **Run the Development Server:**

    bash

    Copy code

    `python manage.py runserver`

### Usage

1.  **Creating an Account:**

    -   Navigate to `/signup/` to create a new account.
.
2.  **Viewing Moon Phases:**

    -   The current moon phase is shown on the homepage along with its properties, such as moonrise, moonset, and illumination percentage.
    -   You can track the moon phase on the **calendar page**, which also links to your journal entries for each day.
3.  **Making a Journal Entry:**

    -   On the moon phase page, you can add a journal entry related to your thoughts or feelings during the current moon phase.
    -   The app automatically associates the entry with the correct moon phase based on the date.

4.  **Updating Your Profile:**

    -   Visit `/profile/<username>/` to view and edit your user information.
### Future Enhancements

-   **Dynamic Calculation of Moon Phases**: Create a calculator that can calculate moon phase based on location.
-   **User Authentication and Security Enhancements**: Implement more robust security measures for user profiles and journal entries.
-   **Update Sytling**: Create an app with all the bells and whistles.

### Wireframes

[Wireframe Sketches](https://www.figma.com/board/E7gCpxC2lOsxxjhdIvZOFv/Moonside-wireframes?node-id=1-257&t=7xodAV6H87KYweHL-1)

### Domain Model (Text Form)

**Entities:**

1.  **User**:

    -   Attributes: `username`, `email`, `password`, `location`, `profile_picture`
    -   Relationships: Can create multiple `JournalEntry` records and view `MoonPhase` data.
2.  **CustomUser** (inherits from `User`):

    -   Additional Attributes: `location`, `profile_picture`
    -   Relationships: A specialized user model that may interact with `JournalEntry` and `MoonPhase`.
3.  **MoonPhase**:

    -   Attributes: `date`, `phase`, `moonrise`, `moonset`, `sunrise`, `sunset`, `illumination`, `uuid`
    -   Relationships: Moon phase data is associated with specific `JournalEntry` instances by date.
4.  **JournalEntry**:

    -   Attributes: `id`, `date`, `entry_text`, `reflect_text`, `intent_text`, `manifest_text`, `uuid`
    -   Relationships: Each entry is created by a `User` and may relate to a specific `MoonPhase` based on date.
5.  **Calendar** (view component):

    -   Attributes: `date`, `month`, `year`, `moon_phases[]`
    -   Relationships: Displays a monthly overview of `MoonPhase` data, with links to related `JournalEntry` instances for each date.

**Relationships**:

-   `User` has a `one-to-many` relationship with `JournalEntry` (each user can create multiple entries).
-   `JournalEntry` has a `one-to-one` relationship with `MoonPhase` by date (each entry corresponds to one moon phase).
-   `Calendar` displays multiple `MoonPhase` records in a grid layout for a month and links each `MoonPhase` to relevant `JournalEntry` records.

This domain model represents the application's primary data relationships and supports functionalities such as personalized entries, viewing moon phases, and calendar-based reflections.

### User Stories
#### User Story 1: Reflective User

**Difficulty**: Medium

**As a reflective user, I want the ability to add journal entries related to specific moon phases to track patterns in my thoughts and moods.**

**Feature Tasks:**

-   Enable users to create a new journal entry for a given moon phase.
-   Automatically associate each entry with the correct moon phase and date.
-   Allow users to view and edit their past entries.

**Acceptance Tests:**

-   Ensure the journal entry form saves the entry under the correct moon phase.
-   Verify that each entry is accurately associated with the selected date and moon phase.
-   Confirm that users can successfully view and update past entries without data loss.

* * * * *

#### User Story 2: Enthusiast

**Difficulty**: Medium

**As an  enthusiast, I want to view the moon phase calendar to see how it aligns with significant dates, such as my birthday, for added insights.**

**Feature Tasks:**

-   Implement a calendar view that displays moon phases for each day.
-   Allow users to navigate to specific months and years on the calendar.
-   Link each calendar day to relevant moon phase details, including rise/set times and illumination.

**Acceptance Tests:**

-   Ensure the calendar view shows accurate moon phases for each day.
-   Check that all moon phase details are accessible from each calendar day.
Stretch:
-   Confirm that users can view moon phase data for historical and future dates.

* * * * *

#### User Story 3: Person of differing locale

**Difficulty**: High

**As a person outside of this locale, I want the ability to see the 3-day forecast for my location.**

**Feature Tasks:**

-   Allow users to identify their location for the api call for the forcast in user model.
-   Allow forecast to save new entries into the database.
-   Make sure ids check out.

**Acceptance Tests:**

-   Confirm that the user is getting their forecast from their user.location data.
-   Confirm that journal entries work with forecast data.

* * * * *

#### User Story 4: Mobile User

**Difficulty**: Medium

**As a mobile user, I want an intuitive, responsive interface to view moon phases and log entries on my phone.**

**Feature Tasks:**

-   Design the interface to be responsive and mobile-friendly.
-   Optimize the calendar view, journal entry forms, and profile sections for mobile.
-   Add mobile navigation features for easy access to different sections.

**Acceptance Tests:**

-   Confirm that the app layout adjusts smoothly for various screen sizes.
-   Ensure all features (calendar, journal entry, profile) are accessible and usable on mobile.
-   Verify that forms and buttons are appropriately sized and spaced for mobile interaction.

* * * * *

#### User Story 5: Visual User

**Difficulty**: Medium

**As a visual user, I want to see and be able to edit all of my previous journal entries.**

**Feature Tasks:**

-   Allow a list view of journal entries protected by user authorization. 
-   CRUD operations on the user journal entries.

**Acceptance Tests:**

-   Verify that users can view and edit/delete their previous entries.
-   Confirm that users can create entries tied to moon phases.

### Attribution / Acknowledgments

-   Thanks to the contributors who have supported this project.
-   Special thanks to `weatherapi.com` for providing moon phase data.
-   Calendar data for this demo was provided by [timeanddate.com](https://www.timeanddate.com/moon/usa/)
-   Moon images provided by [Watercolor Vectors by Vecteezy](https://www.vecteezy.com/free-vector/watercolor)
-   Thank you to this template for provided a base for me to drastically edit => [Railway Template]((https://railway.app/template/AcACbH?referralCode=NC4Tt6))
