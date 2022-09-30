
# cateLinks = [link.find('a').attrs["href"] for link in categories]


# for link in cateLinks:
#     recipesForEachCate = requests.get(link, headers=headers)
#     soup = BeautifulSoup(recipesForEachCate.text, "html.parser")
#     recipes = soup.findAll('div', class_='single-category-card')
#     print("Recipe: ")
#     print(recipes)
#     print('\n')