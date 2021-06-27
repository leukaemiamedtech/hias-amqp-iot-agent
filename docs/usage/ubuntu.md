# Ubuntu Usage

![HIAS AMQP IoT Agent](../img/project-banner.jpg)

# Introduction
This guide will guide you through using the **HIAS AMQP IoT Agent**.

&nbsp;

# Start the Agent

Now you are ready to fire up your HIAS AMQP IoT Agent, to do so use the following command:

``` bash
sudo systemctl start HIAS-AMQP-IoT-Agent.service
```

The Agent will no sit listening for all data coming from the HIAS network using the AMQP protocol. Once it receives data it verifies authorization via HIASBCH and sends the data to HIASCDI & HIASHDI.

# Manage the Agent

To manage the agent you can use the following commands:

``` bash
sudo systemctl restart HIAS-AMQP-IoT-Agent.service
sudo systemctl stop HIAS-AMQP-IoT-Agent.service
```

&nbsp;

# Contributing
Asociación de Investigacion en Inteligencia Artificial Para la Leucemia Peter Moss encourages and welcomes code contributions, bug fixes and enhancements from the Github community.

Please read the [CONTRIBUTING](https://github.com/AIIAL/HIAS-AMQP-IoT-Agent/blob/main/CONTRIBUTING.md "CONTRIBUTING") document for a full guide to forking our repositories and submitting your pull requests. You will also find information about our code of conduct on this page.

## Contributors
- [Adam Milton-Barker](https://www.leukemiaairesearch.com/association/volunteers/adam-milton-barker "Adam Milton-Barker") - [Asociación de Investigacion en Inteligencia Artificial Para la Leucemia Peter Moss](https://www.leukemiaresearchassociation.ai "Asociación de Investigacion en Inteligencia Artificial Para la Leucemia Peter Moss") President/Founder & Lead Developer, Sabadell, Spain

&nbsp;

# Versioning
We use SemVer for versioning.

&nbsp;

# License
This project is licensed under the **MIT License** - see the [LICENSE](https://github.com/AIIAL/HIAS-AMQP-IoT-Agent/blob/main/LICENSE "LICENSE") file for details.

&nbsp;

# Bugs/Issues
We use the [repo issues](https://github.com/AIIAL/HIAS-AMQP-IoT-Agent/issues "repo issues") to track bugs and general requests related to using this project. See [CONTRIBUTING](https://github.com/AIIAL/HIAS-AMQP-IoT-Agent/blob/main/CONTRIBUTING.md "CONTRIBUTING") for more info on how to submit bugs, feature requests and proposals.