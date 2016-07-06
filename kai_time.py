#!/bin/python2

import argparse

ingredients = {}
tobuy = {}
recipes = []

def read_ingredients_file():

    ingred_num = 0
    for line in open('ingredients'):
        stripped = line.strip()
        if len(stripped) == 0 or stripped.startswith('#'):
            continue

        parts = stripped.split(',')
        key = parts[0].strip()
        ingred = (ingred_num, parts[1].strip())
        ingred_num += 1

        ingredients[key] = ingred

def read_recipe(rfile):

    recipes.append(rfile)

    for line in open(rfile):
        stripped = line.strip()
        if len(stripped) == 0 or stripped.startswith('#'):
            continue

        parts = stripped.split(',')
        quantity = float(parts[0])
        key = parts[1].strip()

        if tobuy.has_key(key):
            ingred_count = tobuy[key]
        else:
            if not ingredients.has_key(key):
                raise Exception(
                    'Ingredient key \'%s\' in recipe \'%s\' was not found' \
                            ' in ingredients file' % (key, rfile))
            ingred_count = [0.0, ingredients[key]]

        ingred_count[0] += quantity
        tobuy[key] = ingred_count

def print_shopping_list():

    shop = tobuy.values()
    shop.sort(key=lambda quantity: quantity[1][0])

    print('=== Shopping list ===')
    print('== Remember, responsible trolley operators keep left ==')
    print('')

    for item in shop:
        print('%.1fx %s' % (item[0], item[1][1]))

    print('')
    print('== Generated from recipes ==')

    for recipe in recipes:
        print(recipe)

parser = argparse.ArgumentParser(description='Generate a funky shopping list')
parser.add_argument('recipes', metavar='recipe', type=str, nargs='+')
args = parser.parse_args()

read_ingredients_file()

for recipe in args.recipes:
    read_recipe(recipe)

print_shopping_list()


