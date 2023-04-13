# Code Meta

Code Meta is a GUI application that allows developers to manage and edit notes associated with files.

## Dependencies

The following dependencies are required to run the Project Name application:

- Python 3.8 +

## Installation

1. Clone the Code Meta repository: `git clone https://github.com/YuetChan/code-meta.git`
2. Change to the code-meta directory: `cd /path/to/code-meta`
3. Make the build.sh script executable: `chmod +x ./build.sh`
4. Code Meta icon should show up on show applications/application menu

## Usage

- Open existing projects: Users can open an existing project by reading the s_config.json file for the project name and project ID.
- Create new projects: Users can create new projects, which will generate a s_config.json file that contains Project name and Project ID.
- File tree and text editor: Once a project is opened or created, users can view a file tree and a text editor for editing notes associated with files.
- Text formatting: Users can apply various text formatting options such as bold, italic, underline, left, center, and right alignment, and bullet points to the notes.
- Dangling file searcher: The application provides a search bar and a file list that displays files with dangling notes, which are notes associated with files that are not present in the file tree.
- Auto deletion: When users empty dangling notes, it will remove the associated file from the file list.

## License

This project is licensed under the [License Name] License - see the LICENSE file for details.

## Contact Information

For any questions or inquiries, please contact [Your Name] at [Your Email Address].
