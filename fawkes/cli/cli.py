""" This will serve as the CLI for fawkes """
import argparse
import sys
import os
import logging

# This is so that below import works.  Sets the pwd to home directory
sys.path.append(os.path.realpath("."))

import fawkes.constants.constants as constants

import fawkes.fetch.fetch as fetch
import fawkes.parse.parse as parse
import fawkes.algorithms.algo as algo
import fawkes.email_summary.email_summary_detailed as email_summary_detailed
import fawkes.email_summary.send_email as send_email
import fawkes.datastore.elasticsearch as elasticsearch
import fawkes.slackbot.slackbot as slackbot
import fawkes.algorithms.categorisation.text_match.trainer as text_match_trainer
import fawkes.algorithms.categorisation.lstm.trainer as lstm_trainer
import fawkes.algorithms.similarity.similarity as similarity

from fawkes.cli.fawkes_actions import FawkesActions

def define_arguments(parser):
    # Specify an action
    parser.add_argument(
        "action",
        help="The action that's supposed to be done.",
        type=str,
        choices=[
            FawkesActions.FETCH,
            FawkesActions.PARSE,
            FawkesActions.RUN_ALGO,
            FawkesActions.GENERATE_EMAIL,
            FawkesActions.SEND_EMAIL,
            FawkesActions.PUSH_ELASTICSEARCH,
            FawkesActions.QUERY_ELASTICSEARCH,
            FawkesActions.PUSH_SLACK,
            FawkesActions.GENERATE_TEXT_MATCH_KEYWORDS,
            FawkesActions.TRAIN_LSTM_MODEL,
            FawkesActions.QUERY_SIMILAR_REVIEWS,
        ],
    )
    # Specify app-configs file path
    parser.add_argument(
        "-c", "--fawkes_config",
        help="The path to the fawkes-config.json file.",
        type=str,
        default=constants.FAWKES_CONFIG_FILE,
    )
    # Specify app-configs file path
    parser.add_argument(
        "-a", "--app_config",
        help="The path to the app config json file for a particular app.",
        type=str,
    )
    # Specify query index for elasticsearch query
    parser.add_argument(
        "-q", "--query",
        help="The query index for elasticsearch query",
        type=str,
        default="",
    )
    # Specify response file format for elasticsearch query
    parser.add_argument(
        "-f", "--format",
        help="The response file format for elasticsearch query",
        type=str,
        default=constants.JSON,
    )

def init_logger():
    logging.basicConfig(
        format='%(levelname)s: %(message)s', level=logging.INFO
    )

if __name__ == "__main__":
    # Init the arg parser
    parser = argparse.ArgumentParser()
    # Defining all the arguments
    define_arguments(parser)
    # Extracting all the arguments
    args = parser.parse_args()

    # Depending on the args, we execute the commands.
    action = args.action
    fawkes_config_file = args.fawkes_config
    app_config_file = args.app_config
    query_term = args.query
    query_response_file_format = args.format

    # Initialise the logger
    init_logger()

    if action == FawkesActions.FETCH:
        fetch.fetch_reviews(fawkes_config_file)
    elif action == FawkesActions.PARSE:
        parse.parse_reviews(fawkes_config_file)
    elif action == FawkesActions.RUN_ALGO:
        algo.run_algo(fawkes_config_file)
    elif action == FawkesActions.GENERATE_EMAIL:
        email_summary_detailed.generate_email_summary_detailed(fawkes_config_file)
    elif action == FawkesActions.SEND_EMAIL:
        send_email.send_email(fawkes_config_file)
    elif action == FawkesActions.PUSH_ELASTICSEARCH:
        elasticsearch.push_data_to_elasticsearch(fawkes_config_file)
    elif action == FawkesActions.QUERY_ELASTICSEARCH:
        elasticsearch.query_from_elasticsearch(fawkes_config_file, query_term = query_term, format = query_response_file_format)
    elif action == FawkesActions.PUSH_SLACK:
        slackbot.send_reviews_to_slack(fawkes_config_file)
    elif action == FawkesActions.GENERATE_TEXT_MATCH_KEYWORDS:
        text_match_trainer.generate_keyword_weights(fawkes_config_file)
    elif action == FawkesActions.TRAIN_LSTM_MODEL:
        lstm_trainer.train_lstm_model(fawkes_config_file)
    elif action == FawkesActions.QUERY_SIMILAR_REVIEWS:
        similarity.get_similar_reviews_for_app(app_config_file, query_term, 20)
    else:
        raise Exception("Invalid action!")

