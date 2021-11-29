import os
from . import db
from flask import Flask, jsonify, request
import datetime

from .helpers import get_next_grouping_date, get_table_columns

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/api/info', methods=['GET', 'POST'])
    def api_info():
        """
        Method which could be used to get all existing attrib->value filter options
        """
        table = 'data'

        attributes = get_table_columns(table = table)

        response = [{'attributes':attributes}]

        if len(attributes) == 0:
            raise ValueError("Database not initialized, or data doesn't exist.")


        database = db.get_db()
        for attribute in attributes:
            unique_values_for_attribute_request = "SELECT DISTINCT {attribute} FROM {table};".format(attribute = attribute, table = table)
            values = database.execute(unique_values_for_attribute_request).fetchall()
            values = list(map(lambda row: row[attribute], values))
            response.append({attribute:values})

        return jsonify(response)

    @app.route('/api/timeline', methods=['GET', 'POST'])
    def api_timeline():
        time_format = "%Y-%m-%d"
        table = 'data'
        # TODO: params validaton
        startDate = datetime.datetime.strptime(request.args.get('startDate'), time_format)
        endDate =  datetime.datetime.strptime(request.args.get('endDate'), time_format)
        # cumulative || usual
        Type = request.args.get("Type")
        # weekly || bi-weekly || monthly
        Grouping = request.args.get("Grouping")

        attribute_values = []

        attributes = get_table_columns(table = table)

        for attribute in attributes:
            if request.args.get(attribute) != None:
                attribute_values.append("{attribute} = \"{value}\"".format(attribute = attribute, value=request.args.get(attribute)))


        database = db.get_db()

        # Selecting all data beetween startDate and endDate
        request_data = "SELECT * FROM {table} WHERE timestamp > {startDate} AND timestamp < {endDate} ".format(
            table = table, startDate = startDate.timestamp(), endDate = endDate.timestamp())
        # Adding attribute\value filtering
        request_data =request_data + " AND " +" AND ".join(attribute_values)
        # Order selected data by timestamp
        request_data = request_data + " ORDER BY timestamp"


        data = database.execute(request_data).fetchall()

        # Means no data for this request
        if len(data) == 0:
            return jsonify({'timeline':None})

        # Setting inital data
        current_date = startDate
        next_date = get_next_grouping_date(date = current_date, grouping = Grouping)
        response = {'timeline':[{'date':current_date.strftime(time_format), 'value':0}]}
        
        for data_element in data:
            if data_element['timestamp'] > current_date.timestamp():
                current_date = next_date
                next_date = get_next_grouping_date(date = current_date, grouping = Grouping)
                if Type == 'cumulative':
                    response['timeline'].append({'date':current_date.strftime(time_format), 'value':response['timeline'][-1]['value']})
                elif Type == 'usual':
                    response['timeline'].append({'date':current_date.strftime(time_format), 'value':0})
            response['timeline'][-1]['value'] = response['timeline'][-1]['value'] +1

        return jsonify(response)


    db.init_app(app)
    return app

