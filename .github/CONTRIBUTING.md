# How to Start Contributing to Project Nebulus!

## Table of Contents

- [Setting Up Your Coding Environment](#setting-up-your-coding-environment)
- [Contributing](#contributing)

## Setting Up Your Coding Environment

### Step 1: Get the IDEs
1) Go to https://www.jetbrains.com/shop/eform/students and make a new application. If you already have the [GitHub developer pack](https://education.github.com/pack), you may choose the GitHub tab. This will give you premium for all JetBrains IDEs.
2) Wait for an email from `JetBrains Sales` with an email titled `License Certificate for your JetBrains Educational Pack`. Give it 2 minutes, if its not there wait another 2 minutes. It's usually very quick!
3) Download required Nebulus IDEs. `PyCharm Professional` (Don't get `PyCharm CE/Community Edition`), `WebStorm`, `DataGrip`. Optional IDEs include `IntelliJ Ultimate` and `CLion`

#### Download Links:

- [PyCharm Professional](https://www.jetbrains.com/pycharm/download/)

> Make sure to download Professional, not Community Edition
 
- [WebStorm](https://www.jetbrains.com/webstorm/download/)

- [DataGrip](https://www.jetbrains.com/datagrip/download/)

- [CLion](https://www.jetbrains.com/clion/download/) (optional)

- [IntelliJ Ultimate](https://www.jetbrains.com/intellij/download/) (optional)

> Make sure to download Ultimate, not Community Edition

--- 

### Step 2: Get the GitHub Repository on Your Device

#### Clone the Repository

```bash
$ git clone https://github.com/ProjectNebulus/ProjectNebulus.git
```
---
### Step 3: Configure Username and Password (Optional)

>⚠ WARNING: If you haven't created a Personal Access Token yet, please make one! It is basically your password when using the github api. 

> To create one go to Settings > Developer Settings > [Personal access tokens](https://github.com/settings/tokens)


#### Set Username
```bash
$ git config --global user.name "your username"
```
#### Set Password (Personal Access Token)

##### 1. Caching Credentials With Keychain Access (MacOS ONLY)

1. Open Keychain Access (You can search "Keychain" in spotlight) 
![image](https://user-images.githubusercontent.com/76001641/149199644-91155da4-2cff-46cd-87fa-dd115a459e79.png)
2. In Keychain, search for "github"

3. There will be a few results, click on the one that says "Internet Password"


4. Click the "Show Password" option and enter your computer password to let Keychain have access.

5) Enter Your Personal Access Token in the area where it shows your password.

##### 2. Caching Credentials (Github CLI)

There are quite a few ways to install the Github CLI

You can see them all [here](https://cli.github.com/manual/installation)

__Caching Credentials__
```bash
$ gh auth login
```
- When asked which account you want to login with, choose `Github.com`
- When prompted for your preferred protocol for Git operations, select `HTTPS`.
- When asked if you would like to authenticate to Git with your GitHub credentials, enter `Y`.
- When asked how you would like to authenticate choose `Paste an authentication token` then paste your Personal Access Token

## Contributing

### Code Style

Use our project-specific conventions for code formatting. For example, we use [prettier](https://prettier.io) for JavaScript (and related), [black](https://github.com/psf/black) for Python, etc. There should be scripts already written to do this, such as `npm run format` (prettier).

### Commit Messages

Although not required, please try to follow the [conventional commits specification](https://www.conventionalcommits.org/en/v1.0.0/) for your commits. If not, **write a meaningful commit message to explain what the commit changes.**