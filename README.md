# 🧾 Queue Management System

A role-based **Queue Management Web Application** built using **Django**. This system enables staff and supervisors to handle customer service requests efficiently via a token-based queue mechanism. It includes:

* Real-time dashboard for queue tracking
* Token generation with auto-increment
* Status management (`waiting`, `in-progress`, `completed`)
* Public display view for service status
* Manual token reset option
* Role-based access control

---

## 🚀 Features

### 🔐 Authentication & Roles

* User registration with role selection (Staff, Supervisor)
* Secure login/logout system
* Separate privileges for different roles

### 📊 Dashboard

* View live counts of:

  * Waiting queue
  * In-progress services
  * Completed services
* Token list filtering by status

### 🎫 Token Management

* Generate new service tokens with auto-numbering (`T001`, `T002`, ...)
* Change status to `in-progress` or `completed`
* View recently completed services (latest 10)

### 📺 Public Display View

* Accessible at a separate URL (`/display/`)
* Shows:

  * Now serving customers
  * Recently completed tokens
  * Waiting queue
* Auto-refresh every 10 seconds

