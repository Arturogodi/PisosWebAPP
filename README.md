# PisosWebAPP

## Description

PisosWebAPP is a web application designed to manage and visualize information about apartments. This application allows users to search, filter, and view details of different available apartments.

## Demo Videos

Here are some demo videos showcasing the functionality of PisosWebAPP:

- [Demo Video WEB APP](https://youtu.be/RkmBoka9VSU)
- [Demo Video TFM project END2END](https://youtu.be/sjX1kWD8ExI)

## Project Structure

The project structure is as follows:

### Description of Files and Directories

- **static/**: Contains static files such as CSS, JavaScript, and images.
- **templates/**: Contains the HTML templates of the application.
- **app.py**: Main application file where the Flask application is configured and run.
- **config.py**: Application configuration file.
- **models.py**: Defines the data models used in the application.
- **requirements.txt**: List of dependencies and packages needed to run the application.
- **README.md**: This file, which provides information about the project.

## Installation

To install and run the application locally, follow these steps:

1. Clone the repository:
   `bash
 git clone https://github.com/your_username/PisosWebAPP.git
 cd PisosWebAPP
 `

2. Create a virtual environment and activate it:
   `` bash
 python -m venv venv
 source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ``

3. Install the dependencies:
   `bash
 pip install -r requirements.txt
 `

4. Set up the database (if necessary):
   `bash
 flask db init
 flask db migrate
 flask db upgrade
 `

5. Run the application:
   `bash
 flask run
 `

## Usage

Once the application is running, you can access it in your web browser at `http://localhost:5000`.
After push changes to repository at GitHub main brach automaticaly deploy the web at `https://pisoswebapp-bzc2agd6dpcwfqf9.northeurope-01.azurewebsites.net`.


## Contribution

If you wish to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push your changes to your branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
