# Deployment Configuration Guide

## AWS Elastic Beanstalk Configuration (.elasbean_extensions)

### Purpose
The `.elasbean_extensions` folder contains configuration files to customize your AWS Elastic Beanstalk environment. These YAML files execute commands and set parameters during deployment.

---

### Core File: `python.config`
```yaml
# .ebextensions/python.config
option_settings:
  "aws:elasticbeanstalk:container:python":
    WSGIPath: application:application