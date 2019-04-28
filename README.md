# Wagtail Quick Create

### Wagtail Quick Create offers shortcut links to create objects from models specified in your settings file.

A panel is added to the admin home, offering a type:

![Quick Create Panel example](https://i.imgur.com/ssDighV.png)

Clicking a create link will offer a parent selection for the new item

![Parent selection example](https://i.imgur.com/6w5w6zD.png)

### Configuration

Install using pip:

```[bash]
pip install wagtail-quick-create
```

After installing the module, add `wagtailquickcreate` to your installed apps in your settings file:

```[python]
INSTALLED_APPS = [
    ...
    'wagtailquickcreate',
]
```

Also add the models you would like to create quick links for to your settings file as `'your_app_name.YourModelName'`:

EG:
```
WAGTAIL_QUICK_CREATE_PAGE_TYPES = ['news.NewsPage', 'events.EventPage']
```

If you want the Quick Create links panel to _replace_ the wagtail summary panel, you can set this by adding the following to your settings

```
WAGTAIL_QUICK_CREATE_REPLACE_SUMMARY_PANEL = True
```

If you would like to offer image and or document links, this can also be done by specifying the following in your settings:

```
WAGTAIL_QUICK_CREATE_DOCUMENTS = True
WAGTAIL_QUICK_CREATE_IMAGES = True
```

### Credits/Authors
Concept created by Kate Statton - NYPR [@katestatton](https://twitter.com/katestatton)