# AutoCV
![AutoCV frontend](./src/assets/autocv_frontend.PNG)

All-in-one purpose-built resume and cover letter generator and automation tool, originally designed for Windows - the functionality of the app was refactored to leverage the open source word processor alternative [LibreOffice](https://www.libreoffice.org/) in lieu of Microsoft Word. Ultimately, this has improved the performance of app *significantly* and allowed it to be ported to MacOS and Linux.

## Description
AutoCV is a full-stack web application built with [Vue.js](https://vuejs.org), [Typescript](https://typescriptlang.org) and [Flask](https://flask.palletsprojects.com/) to automate the process of modifying and uploading various different resumes and cover letters for different job applications. The app uses a number of templated fields in set of resumes and cover letter files on the backend, and the user can modify the contents of these fields from the frontend across several configurable options. Finally, the user can submit these changes and leverage the [GitHub REST API](https://docs.github.com/en/rest) for automatically converting these files to PDFs, uploading them to a file storage repository, and downloading them directly from the convenience of the browser.

## Dependencies
The app relies on an active installation of LibreOffice on the host system, along with the installed StarOffice executable (`soffice`) present in the system `PATH`.

### Installation for MacOS
```
brew install --cask libreoffice
```

Add the location of the `soffice` executable to the `PATH` variable.
```
which soffice
/opt/homebrew/soffice/bin
```

### Installation for Windows
Detailed instructions for the Windows installation can be [found in the LibreOffice documentation](https://www.libreoffice.org/get-help/install-howto/windows/).

### Installation for Linux
Detailed instructions for the Linux installation can be [found in the LibreOffice documentation](https://www.libreoffice.org/get-help/install-howto/linux/).

## Build Instructions
The app can be built and run separately, or using the included Docker build staging.

#### Running the frontend separarely
Using NPM
```
npm run dev
```

Using yarn
```
yarn run dev
```

### Running the backend separately
The app uses a `Python` wrapper around the GitHub REST API ([pygithub](https://github.com/PyGithub/PyGithub)) - the library is initialized with a `Personal Access Token` (steps for generating this token can be found [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)), and the token is read from the backend through the `GITHUB_TOKEN` environment variable. 

See more about setting up the backend [here](./src/backend/README.md).

#### Windows environment setup
```
set GITHUB_TOKEN=INSERT_YOUR_PERSONAL_ACCESS_TOKEN_HERE
python server.py
```

#### OSX/Linux environment setup
```
export GITHUB_TOKEN=INSERT_YOUR_PERSONAL_ACCESS_TOKEN_HERE
python server.py
```

OR

```
GITHUB_TOKEN=INSERT_YOUR_PERSONAL_ACCESS_TOKEN_HERE python server.py
```

### Docker staging

#### Building frontend and backend images
```
docker-compose build
```

#### Running Docker images
```
docker-compose up --remove-orphans
```
