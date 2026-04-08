# 🎓 DeviX Connections — by Ram Sir

A private social media platform for coaching students.

## 🚀 Quick Start

### 1. Install Requirements
```bash
pip install django pillow
```

### 2. Setup Database & Admin
```bash
python setup.py
```

### 3. Run Server
```bash
python manage.py runserver
```

### 4. Open in Browser
- **Platform:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 🔐 Admin Credentials (Ram Sir)
| Field | Value |
|-------|-------|
| Username | `` |
| Password | `` |

---

## 👨‍💼 Admin Can (via /admin/):
- **Add Students** → Users → Add User (set username + password)
- **Edit Student Profile** → Profiles → set Student ID
- **Delete Students** → Users → select → Delete
- **Delete Posts** → Posts → select → Delete
- **View all activity**

## ⚠️ Student Restrictions:
- **Cannot** change their Name, Student ID, or Password
- **Can** change: Nickname, Bio, Profile Photo
- **Can** Post, Like, Comment, Follow/Unfollow, Chat

---

## 📁 Project Structure
```
devix/
├── devix_project/       # Django settings & urls
├── core/                # Main app
│   ├── models.py        # Profile, Post, Comment
│   ├── views.py         # All views
│   ├── admin.py         # Admin config
│   ├── templates/core/  # HTML templates
│   └── templatetags/    # Custom tags
├── media/               # Uploaded files
├── manage.py
├── setup.py             # Quick setup script
└── README.md
```

## 🌟 Features
- ✅ Beautiful dark-accented UI with Syne + DM Sans fonts
- ✅ Admin-only user creation (name, ID, password)
- ✅ Students can edit nickname, bio, avatar
- ✅ Post: thoughts, study notes, coaching info, photos, videos, audio
- ✅ Like, comment on posts
- ✅ Follow / Unfollow students
- ✅ Chat with students
- ✅ Student directory with search
- ✅ Profile pages
- ✅ Full Django Admin control for Ram Sir
