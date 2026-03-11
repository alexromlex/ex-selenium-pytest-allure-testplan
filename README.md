# Automated Website Testing (pytest, selenium, allure)

[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-blue?logo=github-actions)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green?logo=selenium)](https://www.selenium.dev/)
[![Allure](https://img.shields.io/badge/Allure-3.x-orange?logo=allure)](https://allurereport.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Overview

A robust black-box automated testing framework for web applications, built with modern tools and practices. This project demonstrates a complete CI/CD testing pipeline with advanced reporting capabilities and cloud integration.

**Live demo:** [View Test Reports](https://alexromlex.github.io/ex-selenium-pytest-allure-testplan/)

## 🚀 Features

- **Black-box Testing Approach** - Tests web applications from an end-user perspective + API
- **Modern Tech Stack** - Python, Pytest, Selenium, and Allure 3
- **Automated CI/CD** - GitHub Actions integration with secure token authentication
- **Smart Test Planning** - Dynamic testplan generation based on metadata
- **Comprehensive Reporting** - Allure reports with history tracking and environment filtering
- **Cloud Integration** - Cloudflare worker for remote test execution triggers
- **Historical Analysis** - Test history preservation and trend visualization
- **GitHub Pages Deployment** - Automatic report publishing

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Core Framework** | Python + Pytest |
| **Browser Automation** | Selenium WebDriver |
| **Reporting** | Allure 3 |
| **CI/CD** | GitHub Actions |
| **Test Environment** | Linux (Debian) |
| **Browser** | Chrome v146.0.7680.71 |
| **Cloud Functions** | Cloudflare Workers |
| **Hosting** | GitHub Pages |

## 🔄 Workflow

1. **Testplan Generator** searches through test metadata
2. **Cloudflare Worker** receives requests and triggers GitHub Actions
3. **GitHub Actions** executes tests with secure GITHUB_TOKEN authentication
4. **Test Execution** runs on Debian Linux with Chrome browser
5. **Metadata Generation** creates comprehensive test documentation
6. **History Tracking** preserves previous test results
7. **Allure Report** generates with custom Testplan Generator integration
8. **Pages Deployment** automatically updates the public report page

## 📈 Test Reports

View detailed test results at:  
🔗 [https://alexromlex.github.io/ex-selenium-pytest-allure-testplan/](https://alexromlex.github.io/ex-selenium-pytest-allure-testplan/)

**Report features:**
- Test execution results with detailed logs
- Historical trends and comparisons
- Environment-based filtering
- Custom testplan visualization
- Failure analysis and screenshots

## 🔐 Security
- All GitHub Actions runs require GITHUB_TOKEN authentication
- Secure environment variables for sensitive data
- Cloudflare worker with request validation

# 📝 Notes
## ⚠️ Educational Purpose
This project is created exclusively for educational purposes to demonstrate:
- Automated testing frameworks
- CI/CD integration
- Cloud-based test execution
- Dynamic test planning
- Reporting and visualization

# ⭐ Support
If you find this project useful or interesting, please consider giving it a star! 
It helps others discover this educational resource.

# 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Made with ❤️ for the testing community
