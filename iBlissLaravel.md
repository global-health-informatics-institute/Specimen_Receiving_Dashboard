# iBliss Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Objectives](#objectives)
3. [Requirements](#requirements)
4. [Installation](#installation)

## Introduction
The iBLIS (Integrated Laboratory Information System) Laravel module is a comprehensive tool designed to streamline laboratory data management. This module facilitates ordering, result reporting, and interfacing with laboratory machines, all through a local and centralized National LIMS (Laboratory Information Management System). In the GHII use case, it is used for simulating the KCH environment.

## Objectives
In the GHII setting, this system is for tracking test statuses and pushing state changes to the ordered tests.

## Requirements
The following are the requirements to replicate the current working state for iBLIS Laravel:

- **Hardware**
  - PC with internet connection
- **Software**
  - Ubuntu OS: Jammy Jelly-22.04 LTS
  - PHP 5.6
  - MySQL 8
  - Chromium browser
  - Terminal
- **Other Requirements**
  - Git
  - Dependencies
  - File and access permissions (Root permissions)

## Installation
For the current setting, the only recommended modules are iBLIS Laravel and iBLIS Reception.

- Choose Working Directory
  Preferably `~/path/to/your/GHII/`

- Clone the iBLIS repo:
  ```sh
  git clone https://github.com/HISMalawi/iBLIS.git
  ```

- Checkout to the development branch:
  ```sh
  git checkout development_1.0
  ```

- Rename all `.php.example` files to `.php` in `app/config`:
  ```sh
  cd app/config
  for file in *.php.example; do mv "$file" "${file%.example}"; done
  ```

- Configure `app/config/database.php`.

- Configure `bootstrap/start.php`:
  - Add the PC name in local for development mode. For example:
    ```php
    $env = $app->detectEnvironment(array(
        'local' => array('ghii'),
    ));
    ```

- Give file system permission to the project folders and its subdirectories:
  ```sh
  # use appropriate commands to set permissions
  ```

- Create the following directories:
  ```sh
  mkdir -p /home/eight/Desktop/GHII/iBLIS/app/storage/sessions
  ```

- Install PHP 5.6:
  ```sh
  sudo apt-get install php5.6
  ```

- Install additional PHP 5.6 modules:
  ```sh
  sudo apt-get install curl mcrypt intl xsl mbstring zip soap gd
  ```

- Make sure PDO is installed and enabled.

- Install Composer 2.2 LTS:
  ```sh
  # download and install Composer
  ```

- Run Composer update:
  ```sh
  composer update
  ```

- Edit the MySQL config file to use native auth over the `cache_password_sha`:
  ```sh
  # specify the file and the property to set
  ```

- Run the following Artisan commands:
  ```sh
  php artisan create
  php artisan migrate
  php artisan db:seed
  ```

- Finally, start the development server:
  ```sh
  php artisan serve
  ```
