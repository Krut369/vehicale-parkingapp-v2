# Vehicle Parking App v2

A full-stack web application for managing vehicle parking lots, reservations, and analytics. Built with **Flask** (backend) and **Vue 3 + Vite** (frontend). Supports user and admin roles, WhatsApp notifications, CSV export, and analytics dashboards.

---

## Demo Video

<details>
    <summary>Click to expand video demo</summary>
    <video src="2.mp4" controls width="100%"/>
</details>

---

## Project Structure

```
vehicle-parking-app-v2/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes/
│   │   ├── services/
│   │   └── tasks/
│   ├── instance/
│   │   └── database.db
│   ├── celery_worker.py
│   ├── celery_beat.py
│   ├── requirements.txt
│   └── run.py
│
└── frontend/
    ├── src/
    ├── public/
    ├── package.json
    ├── vite.config.ts
    └── ...
docker-compose.yml
```

---

## Features

- **User Dashboard:** Book parking spots, view and export reservation history.
- **Admin Dashboard:** Manage lots, users, view reservations, and analytics.
- **WhatsApp Notifications:** Booking, reminders, and summaries (via Fonnte API).
- **CSV Export:** Download reservation history.
- **Analytics:** Charts for usage and revenue.
- **Role-based Routing:** Separate views for users and admins.
- **Responsive UI:** Built with Bootstrap 5.
- **Celery Tasks:** Asynchronous and scheduled jobs (reminders, reports).
- **Dockerized Deployment:** All components run in isolated containers.
- **Redis Integration:** Fast message broker for Celery.

---

## Dockerized Workflow

All components (backend, frontend, Celery worker/beat, Redis) are containerized and orchestrated via Docker Compose.

### Quick Start

1. **Build and run all services:**
    ```sh
    docker-compose up --build
    ```

2. **Access the app:**
    - **Frontend:** [http://localhost:5173](http://localhost:5173)
    - **Backend API:** [http://localhost:5000](http://localhost:5000)

3. **Stop all containers:**
    ```sh
    docker-compose down
    ```

---

## Getting Started (Manual)

### Prerequisites

- Python 3.9+
- Node.js 18+
- Redis (for Celery tasks)

---

## Backend Setup

1. **Install dependencies:**
    ```sh
    cd backend
    pip install -r requirements.txt
    ```

2. **Run the backend server:**
    ```sh
    python run.py
    ```
    - The API will be available at `http://localhost:5000`.

3. **Celery Worker & Beat (for scheduled tasks):**
    In separate terminals:
    ```sh
    celery -A celery_worker.celery worker --loglevel=info
    celery -A celery_beat.celery beat --loglevel=info
    ```
    - Requires Redis running locally (`redis://localhost:6379/0`).

---

## Frontend Setup

1. **Install dependencies:**
    ```sh
    cd frontend
    npm install
    ```

2. **Run the development server:**
    ```sh
    npm run dev
    ```
    - The app will be available at [http://localhost:5173](http://localhost:5173).

3. **Build for production:**
    ```sh
    npm run build
    ```

---

## Environment Variables

- **Frontend:** See [frontend/.env](frontend/.env)
    ```
    VITE_API_BASE=http://localhost:5000
    ```
- **Backend:** Uses SQLite by default (`instance/database.db`). Update `SQLALCHEMY_DATABASE_URI` in [backend/app/__init__.py](backend/app/__init__.py) if needed.

---

## Default Accounts

- **Admin:**  
  - Username: `anand`  
  - Password: `anand123`
- **User:**  
  - Username: `user`  
  - Password: `user123`

---

## API Overview

- **Auth:** `/api/auth/register`, `/api/auth/login`
- **User:** `/api/user/available-lots`, `/api/user/book`, `/api/user/history/<user_id>`, `/api/user/export-csv`
- **Admin:** `/api/admin/lots`, `/api/admin/users`, `/api/admin/reservations`, `/api/admin/spot-status`

See [backend/app/routes/](backend/app/routes/) for full route implementations.

---

## WhatsApp Integration

- Uses [Fonnte API](https://fonnte.com/) for WhatsApp notifications.
- Configure API token in [`app/services/whatsapp_service.py`](backend/app/services/whatsapp_service.py).

---

## Customization

- **Frontend UI:** Edit Vue components in [frontend/src/](frontend/src/).
- **Backend Logic:** Edit Flask routes and models in [backend/app/](backend/app/).

---

## License

This project is for educational/demo purposes. See individual dependencies for their licenses.

---

## Credits

- [Vue 3](https://vuejs.org/), [Vite](https://vitejs.dev/), [Bootstrap 5](https://getbootstrap.com/), [Chart.js](https://www.chartjs.org/)
- WhatsApp integration via [Fonnte API](https://fonnte.com/)

---

## Contact

For questions or support, please open an issue or contact the project maintainer:

- **Email:** [krutarthsolanki9@gmail.com](mailto:krutarthsolanki9@gmail.com)
- **GitHub:** [Krut369](https://github.com/Krut369)
