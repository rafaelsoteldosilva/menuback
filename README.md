# Restaurant Digital Menu Platform — Backend

Backend for a browser-based restaurant digital menu platform built with Django.

This project provides the server-side foundation for a restaurant menu system where customers can browse a digital menu online and restaurant staff can manage categories, dishes, reviews, deliveries, users, preferences, and payment-related flows.

---

## Overview

This backend was built to support a digital menu solution for restaurants. The goal of the system is to allow customers to access a restaurant menu directly from the browser, while giving restaurant staff a private management environment for maintaining menu content and related operational settings.

This repository represents the backend of that solution and demonstrates backend architecture, workflow-oriented business logic, data handling, and integration support for a React frontend.

[Please click here to go to the portfolio](https://www.google.com)

---

## Business Problem

A restaurant digital menu is not only a UI problem.

A real solution also needs a backend capable of:

- managing menu content
- organizing categories and dishes
- handling restaurant users
- supporting review-related flows
- configuring deliveries
- managing preferences
- protecting restricted operations
- supporting payment-related flows
- controlling staged changes before publication

This backend was built to address those needs.

---

## What This Project Demonstrates

This project demonstrates my ability to:

- build a Django backend for a real-world business-oriented web application
- organize server-side logic beyond basic CRUD
- model workflow-based behavior such as publish/discard operations
- support authentication and restricted operations
- structure payment-related backend flows
- prepare preload/setup logic for development and testing
- support a frontend application through clear backend responsibilities

---

## Main Features

### Core Features

- Menu-related backend operations
- Category and dish data handling
- Restaurant user management support
- Review-related backend support
- Delivery-related backend support
- Restaurant preferences/configuration support
- Login and authorization handling
- Preloaded setup data

### Workflow-Oriented Features

This project includes business-logic utilities for staged editing flows, including:

- menu editing publish/discard
- menu sorting publish/discard
- preferences editing publish/discard
- restaurant deliveries editing publish/discard
- restaurant users editing publish/discard
- reviews editing publish/discard

This is important because it shows the backend handles business workflows, not just direct record edits.

### Payment-Related Features

The project structure also includes payment-related backend support through:

- `payment_views.py`
- payment templates under `templates/webpay_plus/`
- additional template support under `templates/othergateways/`

If needed for portfolio use, this can be described as backend support for payment flows and payment-related server-side processing.

---

## Tech Stack

- Python
- Django
- Django ORM
- Django Templates
- REST-style backend structure
- Utility-based business logic modules
- Image hostings like Cloudinary
- Web protection against hacking using tokens

---

## Backend Architecture

The backend is organized around several main responsibilities.

### Main areas of the codebase

- `models.py`  
  Core application data model definitions.

- `views.py`  
  Main backend endpoint logic.

- `authorization_views.py`  
  Authorization-related request handling.

- `loggin_views.py`  
  Login-related backend logic.

- `payment_views.py`  
  Payment-related request handling and server-side flow support.

- `serializer.py`  
  Data serialization for communication with the frontend.

- `utils/`  
  Business logic helpers and workflow modules, especially publish/discard operations and supporting procedures.

- `complete_objects/`  
  Higher-level composed objects such as menu and review-related structures.

- `templates/`  
  Payment and gateway-related HTML templates.

- `migrations/`  
  Database schema evolution, including preload-related migrations.

- `specific_files/`  
  Backend-side specific files and resources.

This structure reflects a backend that supports a broader product workflow, not only isolated endpoints.

---

## Project Structure

```bash
MENUBACK
├─ menuproject/
│  ├─ api/
│  │  ├─ complete_objects/
│  │  │  ├─ All_Reviews_Class.py
│  │  │  └─ Menu_Class.py
│  │  ├─ migrations/
│  │  │  ├─ __init__.py
│  │  │  ├─ 0001_initial.py
│  │  │  └─ 0002_preload_data.py
│  │  ├─ specific_files/
│  │  │  └─ DigitalMenuLogo.py
│  │  ├─ templates/
│  │  │  ├─ othergateways/
│  │  │  └─ webpay_plus/
│  │  │     ├─ commit.html
│  │  │     ├─ error.html
│  │  │     ├─ pay.html
│  │  │     └─ payment_failed.html
│  │  ├─ utils/
│  │  │  ├─ amount_To_Pay.py
│  │  │  ├─ check_current_user_id_and_random.py
│  │  │  ├─ constants_and_strings.py
│  │  │  ├─ Encryption.py
│  │  │  ├─ First_Month_Ammount_To_Pay.py
│  │  │  ├─ Menu_Editing_Publish_or_Discard.py
│  │  │  ├─ Menu_Sort_Editing_Publish_or_Discard.py
│  │  │  ├─ Preferences_Editing_Publish_or_Discard.py
│  │  │  ├─ Restaurant_Deliveries_Editing_Publish_or_Discard.py
│  │  │  ├─ Restaurant_Users_Editing_Publish_or_Discard.py
│  │  │  ├─ Reviews_Editing_Publish_or_Discard.py
│  │  │  └─ Useful_procedures.py
│  │  ├─ __init__.py
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ authorization_views.py
│  │  ├─ loggin_views.py
│  │  ├─ models.py
│  │  ├─ payment_views.py
│  │  ├─ serializer.py
│  │  ├─ test.py
│  │  ├─ urls.py
│  │  └─ views.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ static/
├─ staticfiles/
├─ venv/
├─ manage.py
├─ preloaded_data.py
├─ requirements.txt
└─ README.md
```
