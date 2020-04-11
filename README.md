## Interview project

### Data scientist / ML Engineer assignment - Cyril LAY

#### Description

As a part of an interview process, I developed this module to identify the bot traffic based on a log file of the HTTP requests to an Apache server. 

It contains two parts :
- A PDF file, answering the questions provided by the company about a white paper available here : [MODELING A SESSION-BASED BOTS’ ARRIVAL PROCESS
AT A WEB SERVER](http://www.scs-europe.net/dlib/2017/ecms2017acceptedpapers/0605-dis_ECMS2017_0126.pdf), and giving explanations about the code of part two.
- The basic code of a bot detection POC

#### Usage (Mac OS)

- Ensure you are using python 3.7+
- Install poetry with `brew install poetry`
- Extract the contents of the zip file
- Download the `access.log` file from [here](http://www.almhuette-raith.at/apache-log/access.log) and place it at the root level of the project
- Go to the root level of the project with `cd bot-detection`
- From the module folder, install the module dependencies with `poetry install`
- Run the main script with `poetry run python3 src/main.py`. 

This will print a list of IPs detected as having generated bot traffic at some point. The last print statement can be uncommented to see the requests performed by the bot IPs.
If ran with the full data, the script takes around 30 seconds to run on a MacBook Pro (i5 2.3 Ghz, 16GB Ram). It is possible to run it with a subset of the data by modifying the date argument of `parse_log_file` in `main.py`.

To run the notebook :
- Install jupyterlab with `pip3 install jupyterlab`
- Activate the environment with `poetry shell` and start the jupyter lab with `jupyter lab`.

#### Testing

To run the tests,
- Activate the environment with `poetry shell`
- From the project root, run `python -m unittest`  

#### Next steps

- Like in the paper, implement the initial phase and final phase to build the sessions, it is currently not done
- Further analysis should be performed on the implemented rules to ensure no false positives are flagged, and a minimum of positives is missed
- For now, the script only prints the IPs and doesn't take any further action.
 In a real world scenario, the list of IPs could be inserted into a database to be regularly cached at the Apache server
  level, for example (more information about dynamic blacklisting [here](https://stackoverflow.com/questions/4676954/dynamically-update-apache-config-allow-from-ip-without-a-restart-reload))
- In the output dataframe, boolean columns should be added for each IP, to know which condition(s) it matched to be flagged as a bot
- If the requests are to be analysed from a
 file (versus a stream), the job could be scheduled in something like Airflow. It would be good to
  avoid scheduling the analysis directly on the instance running the server. 
  The best would be to schedule it in a container (that would have access to the log file) 
  managed by Airflow or Kubernetes for example
- Explore other types of blocking aside from IP-blocking : user-agent, cookies, request method etc (interesting ideas at https://perishablepress.com/eight-ways-to-blacklist-with-apaches-mod_rewrite/)
- Explore and implement relevant ad fraud rules : https://www.criteo.com/insights/best-practices-combating-click-fraud-data-series-part-2/
- Add installation instructions for other platforms (Windows, Ubuntu)
- Increase test coverage
- For now, the module doesn't do a distinction between good and bad bots, this distinction should be added to prevent blocking good bots such as search engine crawlers.