 Steps to run the application:
 1. Start the Docker container: `docker-compose up`
 2. Run the two scripts to fill the mongo db (locally):
    - `python blog_data_download.py`
    - `python save_turbine_data.py`
 3. Access FastAPI docs at http://localhost:8000/docs in the web browser
 4. Access http://localhost:3000/ in the web browser
 