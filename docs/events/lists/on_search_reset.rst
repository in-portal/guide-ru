OnSearchReset
=============
`Data Source`_

.. include:: /includes/not_finished.rst

Данное событие инициализирует объект ``kSearchHelper``, с помощью которого осуществляется сброс фильтров поиска на
стандартном списке в административной панели.

Вызывается из шаблона
---------------------

Данное событие вызывается при нажатии на кнопку сброса поиска на стандартной панели списков в административной
панели. Данное событие также вызывается при нажатии клавиши "escape" на фрейме стандартного списка в
административной панели.

Потенциальное применение
------------------------

Данное событие вызвать для удаления следующих переменных из сессии:

- ``<prefix_special>_search_filter``
- ``<prefix_special>_search_keyword``

из таблицы :doc:`/database/table_structure/persistant_session_data`:

- ``<prefix_special>_custom_filter``

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnSearchReset
