OnResetSorting
==============
`Data Source`_

.. include:: /includes/not_finished.rst

Данное событие вызывается из вызова JavaScript функции ``submit_event``.

Вызывается из шаблона
---------------------

Данное событие вызывается при выборе пункта "Default" подраздела "Sort" в меню "View" на списке административной панели.

Потенциальное применение
------------------------

Данное событие может быть использовано для удаления из сессии следующих переменных:

- ``<prefix_special>_Sort1``
- ``<prefix_special>_Sort1_Dir``
- ``<prefix_special>_Sort2``
- ``<prefix_special>_Sort2_Dir``

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnResetSorting
