import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.tasteofhome.com/recipes/dishes-beverages/cakes/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

data = []
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
categories = soup.findAll('div', class_='item')


def getAllShortRecipeOfCategory(link, result):
    count = 0
    print('Scrawling: ', link)
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    shortRecipes = soup.findAll('div', class_='single-category-card')
    for shortRecipe in shortRecipes:
        count += 1
        name = shortRecipe.find('h2', class_='entry-title h4').text
        print('     Scrawling recipe: ', name)
        try:
            excerpt = shortRecipe.find(
                'div', class_='category-card-excerpt').find('p').text
        except:
            excerpt = ''
        recipeLink = shortRecipe.find(
            'div', class_='category-card-content').find('a').attrs['href']
        # get recipe detail
        recipeDetail = getRecipeDetail(recipeLink)

        result.append({
            "count": count,
            "name": name,
            "link": link,
            "excerpt": excerpt,
            "detail": recipeDetail, })
    try:
        nextPageLink = soup.find('a', class_='next page-numbers').attrs['href']
        print('         Next page: ', nextPageLink)
        getAllShortRecipeOfCategory(nextPageLink, result)
    except:
        pass


def getRecipeDetail(link):
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        time = soup.find('div', class_='total-time').find('p').text
        makes = soup.find('div', class_='makes').find('p').text
        ingredients = [ingredient.text for ingredient in soup.find(
            'ul', class_='recipe-ingredients__list recipe-ingredients__collection splitColumns').findAll('li')]
        direction = [direction.find('span').text for direction in soup.findAll(
            'li', class_='recipe-directions__item')]
        nutrition = soup.find(
            'div', class_='recipe-nutrition-facts mobile-expand-section').find('p').text
    except:
        return {}

    return {
        "time": time,
        "makes": makes,
        "ingredients": ingredients,
        "direction": direction,
        "nutrition": nutrition,
    }


for category in categories:
    categoryName = category.find('a').attrs['data-name']
    link = category.find('a').attrs["href"]
    print('Crawling short recipes of category: ', categoryName)
    shortRecipeList = []
    getAllShortRecipeOfCategory(link, shortRecipeList)
    categoryList = {
        "categoryName": categoryName,
        # "link": link,
        "recipe": shortRecipeList,
    }


data.append(categoryList)


json_object = json.dumps(data, indent=4)
with open("data.json", "w") as outfile:
    outfile.write(json_object)

# cateLinks = [link.find('a').attrs["href"] for link in categories]


# for link in cateLinks:
#     recipesForEachCate = requests.get(link, headers=headers)
#     soup = BeautifulSoup(recipesForEachCate.text, "html.parser")
#     recipes = soup.findAll('div', class_='single-category-card')
#     print("Recipe: ")
#     print(recipes)
#     print('\n')
