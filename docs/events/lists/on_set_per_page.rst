OnSetPerPage
============
`Data Source`_

.. include:: /includes/not_finished.rst

Данное событие вызывается из вызова JavaScript функции ``set_per_page``. Устанавливает значение ``per_page``
для списка.

Потенциальное применение
------------------------

Данное событие может быть использовано для парного сохранения следующих переменных в сессию и в таблицу
:doc:`/database/table_structure/persistant_session_data`:

- ``<prefix_special>_PerPage``
- ``<prefix_special>_PerPage``

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnSetPerPage
