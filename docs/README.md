# In-Portal Developers Guide

## Preparations

1. install [Sphinx](http://sphinx-doc.org/): `pip install -U sphinx`
2. install [Read the Docs Sphinx Theme](https://github.com/snide/sphinx_rtd_theme): `pip install -U sphinx_rtd_theme`
3. install [sphinx-autobuild](https://pypi.python.org/pypi/sphinx-autobuild/0.2.3): `pip install -U sphinx-autobuild`

## Automatic building

1. run `make livehtml` in the `docs` folder
2. open `http://localhost:8000/` to view the documentation

Thanks to the __sphinx-autobuild__ the documentation will be automatically built on every change and all browsers,
where it's opened will be reloaded automatically as well.

## One-time building

1. run `make html` in the `docs` folder
2. open `docs/build/html` folder in your browser

## Cross-references

```rst
:ref:`toolbar_button_sample` - the "sample" parameter during Admin Console toolbar button declaration
:ref:`tree_section_sample` - the "sample" parameter in the Admin Console section declaration
:ref:`element_ch_sample` - the "sample" parameter in the Admin Console "combined_header" template block declaration
:ref:`const_sample` - the "sample" constant
:ref:`url_sample` - the "sample" parameter of the "kApplication::HREF" method
:ref:`env_sample` - the "sample" fragment of the environment variable
:ref:`rc_sample` - the "sample" parameter during class registration in the unit config
:ref:`uc_sample` - the "sample" unit config option
:ref:`fmt_class_sample` - the "sample" formatter class
:ref:`tfd_sample` - the "sample" table field declaration parameter
:ref:`fmt_sample` - the "sample" formatter parameter
:ref:`app_cp_sample` - the "sample" parameter of the "kApplication::CheckPermission" method
:ref:`tag_cp_sample` - the "sample" parameter of the "m_CheckPermission" template tag
:ref:`tc_Category_sample` - the "sample" column of the "Category" database table
:ref:`tc_Language_sample` - the "sample" column of the "Language" database table
:ref:`tc_PortalGroup_sample` - the "sample" column of the "PortalGroup" database table
:ref:`tc_Theme_sample` - the "sample" column of the "Theme" database table
:ref:`tc_UserSession_sample` - the "sample" column of the "UserSession" database table
:ref:`cfg_sample` - the "sample" configuration variable
```
