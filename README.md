# Electra: Online Voting Platform

Electra is a robust and intuitive Online Voting Platform designed to streamline the voting process and empower individuals and organizations to make collective decisions. Whether you're conducting elections, surveys, or polls, Electra provides a secure and efficient platform for online voting.

## Features

- Easy-to-use interface for creating and managing voting sessions
- Secure user authentication and data encryption
- Real-time vote tracking and result visualization
- Customizable voting options and configurations
- Mobile-friendly design for seamless access on any device
- User-friendly administration panel for managing users and votes
- Flexible and scalable architecture to handle high volumes of votes

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hengkp/electra-voting-platform.git
   ```
2. Setup virtual environment
   ```bash
   python3 -m venv electra
   ```
3. Activate virtual environment
   ```bash
   source electra/bin/activate
   ```
2. Install the required dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
3. Configure the database settings in config.py.
4. Run the application:
   ```bash
   python3 app.py
   ```
5. Access the application in your web browser:
   ```
   http://localhost:5000
   ```

## Demo

You can try out the demo version of the "Electra: Online Voting Platform" by visiting the GitHub Pages site for this project: [electra-voting-platform Demo](https://heng.pythonanywhere.com/)

The demo allows you to explore the features and functionality of the online voting platform. Please note that the demo may not have all the capabilities of a production-ready deployment.

To access the admin panel in the demo version, use the following credentials:

- Username: `admin`
- Password: `password123`

Feel free to create new accounts, vote on topics, and explore the various features of the platform.

Please keep in mind that the demo version is for demonstration purposes only and may not be actively monitored or maintained. For a fully functional and secure deployment, it is recommended to set up the platform on your own server or hosting environment.


## Contributing

We welcome contributions from the open-source community! If you'd like to contribute to Electra, please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Make your modifications.
Commit and push your changes to your forked repository.
Submit a pull request detailing your changes and any necessary information.
Please ensure that your code adheres to the existing coding style and conventions.

## License

This project is licensed under the **[_MIT License_](https://opensource.org/licenses/MIT)**.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/): A lightweight and versatile web framework used for building the application.
- [Bootstrap](https://getbootstrap.com/): A popular CSS framework used for the responsive design and styling of the user interface.
- [Font Awesome](https://fontawesome.com/): An iconic font and CSS toolkit used for the icons in the application.
- [SQLAlchemy](https://www.sqlalchemy.org/): A powerful and flexible Object-Relational Mapping (ORM) library for working with databases.
- [Jinja](https://jinja.palletsprojects.com/): A templating engine for Python used for generating dynamic HTML pages.
- [OpenSSL](https://www.openssl.org/): A robust cryptographic library used for secure data encryption and decryption.
- [jQuery](https://jquery.com/): A fast and feature-rich JavaScript library used for client-side interactions and DOM manipulation.

Special thanks to the contributors and maintainers of these open-source projects for their valuable tools and resources that made the development of Electra possible.
