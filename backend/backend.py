#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import tempfile
import hashlib
import sqlite3
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from flask import Flask, request, send_from_directory
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['APP_NAME'] = 'hueman-backend'
app.config['UPLOAD_FOLDER'] = os.path.join(
    tempfile.gettempdir(), app.config['APP_NAME'], 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['DB_PATH'] = os.path.join(
    tempfile.gettempdir(), app.config['APP_NAME'], 'database.sqlite3')
DATABASE = None


def match(list_1, list_2):
    THRESHOLD = 18
    
    def calc_diff(color_1, color_2):
        color_1_lab = convert_color(sRGBColor.new_from_rgb_hex(color_1), LabColor)
        color_2_lab = convert_color(sRGBColor.new_from_rgb_hex(color_2), LabColor)
        delta_e = delta_e_cie2000(color_1_lab, color_2_lab)
        return delta_e

    for i in range(len(list_1)):
        if not (calc_diff(list_1[i], list_2[i]) < THRESHOLD):
            return False
    return True

    # primaryColor_1 = list_1[0]
    # secondaryColor_1 = list_1[1]
    # tertiaryColor_1 = list_1[2]
    # primaryColor_2 = list_2[0]
    # secondaryColor_2 = list_2[1]
    # tertiaryColor_2 = list_2[2]

    # diff_1 = calc_diff(primaryColor_1, primaryColor_2)
    # print('delta_e of %s and %s is %s' % (primaryColor_1, primaryColor_2, diff_1))
    # diff_2 = calc_diff(secondaryColor_1, secondaryColor_2)
    # print('delta_e of %s and %s is %s' % (secondaryColor_1, secondaryColor_2, diff_2))
    # diff_3 = calc_diff(tertiaryColor_1, tertiaryColor_2)
    # print('delta_e of %s and %s is %s' % (tertiaryColor_1, tertiaryColor_2, diff_3))
    # return (diff_1 < THRESHOLD_1) and (diff_2 < THRESHOLD_2) and (diff_3 < THRESHOLD_3)


@app.route('/search', methods=['POST'])
def search():
    global DATABASE

    def create_return_obj(row, tags_list):
        return {
            'fileName': row[0],
            'caption': row[1],
            'category': row[2],
            'tags': tags_list,
            'primaryColor': row[3],
            'secondaryColor': row[4],
            'tertiaryColor': row[5],
        }

    content = request.get_json()
    primary_color = content['primaryColor']
    secondary_color = content['secondaryColor']
    tertiary_color = content['tertiaryColor']
    selected_category = content['selectedCategory']
    selected_tags = content['selectedTags']

    matches = []

    if selected_category and selected_tags and primary_color and secondary_color and tertiary_color:
        filenames = []
        for tag in selected_tags:
            filenames += [r[0] for r in DATABASE.execute('SELECT fileName FROM tags WHERE tag = ?', [tag])]

        for filename in filenames:
            DATABASE_CUR = DATABASE.cursor()
            DATABASE_CUR.execute('SELECT * FROM colors WHERE fileName = ? AND category = ?', [filename, selected_category])
            row = DATABASE_CUR.fetchone()

            color_list_1 = [primary_color, secondary_color, tertiary_color]
            color_list_2 = [row[3], row[4], row[5]]

            if match(color_list_1, color_list_2):
                target_tags = [r[0] for r in DATABASE.execute('SELECT DISTINCT tag FROM tags WHERE fileName = ?', [filename])]
                obj = create_return_obj(row, target_tags)
                matches.append(obj)

    elif not(selected_category and selected_tags) and primary_color and secondary_color and tertiary_color:
        for row in DATABASE.execute('SELECT * FROM colors'):
            color_list_1 = [primary_color, secondary_color, tertiary_color]
            color_list_2 = [row[3], row[4], row[5]]

            if match(color_list_1, color_list_2):
                target_tags = [r[0] for r in DATABASE.execute('SELECT DISTINCT tag FROM tags WHERE fileName = ?', [row[0]])]
                obj = create_return_obj(row, target_tags)
                matches.append(obj)

    elif not(selected_category and selected_tags) and primary_color:
        for row in DATABASE.execute('SELECT * FROM colors'):
            color_list_1 = [primary_color]
            color_list_2 = [row[3]]

            if match(color_list_1, color_list_2):
                target_tags = [r[0] for r in DATABASE.execute('SELECT DISTINCT tag FROM tags WHERE fileName = ?', [row[0]])]
                obj = create_return_obj(row, target_tags)
                matches.append(obj)

    elif not(selected_category and selected_tags) and secondary_color:
        for row in DATABASE.execute('SELECT * FROM colors'):
            color_list_1 = [secondary_color]
            color_list_2 = [row[4]]

            if match(color_list_1, color_list_2):
                target_tags = [r[0] for r in DATABASE.execute('SELECT DISTINCT tag FROM tags WHERE fileName = ?', [row[0]])]
                obj = create_return_obj(row, target_tags)
                matches.append(obj)

    elif not(selected_category and selected_tags) and tertiary_color:
        for row in DATABASE.execute('SELECT * FROM colors'):
            color_list_1 = [tertiary_color]
            color_list_2 = [row[5]]

            if match(color_list_1, color_list_2):
                target_tags = [r[0] for r in DATABASE.execute('SELECT DISTINCT tag FROM tags WHERE fileName = ?', [row[0]])]
                obj = create_return_obj(row, target_tags)
                matches.append(obj)

    elif selected_category and selected_tags:
        filenames = []
        for tag in selected_tags:
            filenames += [r[0] for r in DATABASE.execute('SELECT fileName FROM tags WHERE tag = ?', [tag])]

        for filename in filenames:
            DATABASE_CUR = DATABASE.cursor()
            DATABASE_CUR.execute('SELECT * FROM colors WHERE fileName = ? AND category = ?', [filename, selected_category])
            row = DATABASE_CUR.fetchone()
            target_tags = [r[0] for r in DATABASE.execute('SELECT DISTINCT tag FROM tags WHERE fileName = ?', [filename])]
            obj = create_return_obj(row, target_tags)
            matches.append(obj)

    elif selected_tags:
        filenames = []
        for tag in selected_tags:
            filenames += [r[0] for r in DATABASE.execute('SELECT fileName FROM tags WHERE tag = ?', [tag])]

        for filename in filenames:
            DATABASE_CUR = DATABASE.cursor()
            DATABASE_CUR.execute('SELECT * FROM colors WHERE fileName = ?', [filename])
            row = DATABASE_CUR.fetchone()

            target_tags = [r[0] for r in DATABASE.execute('SELECT DISTINCT tag FROM tags WHERE fileName = ?', [filename])]
            obj = create_return_obj(row, target_tags)
            matches.append(obj)

    elif selected_category:
        for row in DATABASE.execute('SELECT * FROM colors WHERE category = ?', [selected_category]):
            target_tags = [r[0] for r in DATABASE.execute('SELECT DISTINCT tag FROM tags WHERE fileName = ?', [row[0]])]
            obj = create_return_obj(row, target_tags)
            matches.append(obj)

    else:
        for row in DATABASE.execute('SELECT * FROM colors'):
            target_tags = [r[0] for r in DATABASE.execute('SELECT DISTINCT tag FROM tags WHERE fileName = ?', [row[0]])]
            obj = create_return_obj(row, target_tags)
            matches.append(obj)

    return json.dumps(matches)


@app.route('/getsearchdata', methods=['GET'])
def get_search_data():
    global DATABASE
    tags_list = [row[0] for row in DATABASE.execute('SELECT DISTINCT tag FROM tags')]
    cats_list = [row[0] for row in DATABASE.execute('SELECT DISTINCT category FROM colors')]
    return json.dumps({
        'categoryItems': cats_list,
        'tagItems': tags_list,
    })


@app.route('/postdata', methods=['POST'])
def post_data():
    global DATABASE
    content = request.get_json()

    DATABASE.execute('INSERT INTO colors VALUES (?, ?, ?, ?, ?, ?)', [
        content['fileName'],
        content['caption'],
        content['category'],
        content['primaryColor'],
        content['secondaryColor'],
        content['tertiaryColor']]
    )
    for tag in content['tags']:
        DATABASE.execute(
            '''
            INSERT INTO tags VALUES (?, ?)
            ''',
            [tag, content['fileName']])

    DATABASE.commit()
    return "sweet success!"


@app.route('/upload', methods=['POST'])
def upload_file():
    file_obj = request.files['file']
    filename, file_extension = os.path.splitext(file_obj.filename)
    file_contents = file_obj.read()
    # filename = xxhash.xxh64(file_contents).hexdigest() + file_extension
    filename = hashlib.md5(file_contents).hexdigest() + file_extension
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'wb') as outfile:
        outfile.write(file_contents)
    return filename


@app.route('/uploads/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except Exception as e:
        pass


def initialize_database():
    global DATABASE
    DATABASE = sqlite3.connect(app.config['DB_PATH'], check_same_thread=False)
    DATABASE.execute(
        '''
        CREATE TABLE IF NOT EXISTS 'tags' (
            'tag' TEXT NOT NULL,
            'fileName' TEXT NOT NULL,
            UNIQUE(tag, fileName)
        );
        '''
    )
    DATABASE.execute(
        '''
        CREATE TABLE IF NOT EXISTS 'colors' (
            'fileName' TEXT NOT NULL UNIQUE,
            'caption' TEXT NOT NULL,
            'category' TEXT NOT NULL,
            'primaryColor' TEXT NOT NULL,
            'secondaryColor' TEXT NOT NULL,
            'tertiaryColor' TEXT NOT NULL
        );
        '''
    )
    DATABASE.commit()


def close_database():
    global DATABASE
    DATABASE.commit()
    DATABASE.close()


if __name__ == '__main__':
    initialize_database()
    print("Images will be saved to %s" % app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
    close_database()
