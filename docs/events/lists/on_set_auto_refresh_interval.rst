OnSetAutoRefreshInterval
========================
`Data Source`_

.. include:: /includes/not_finished.rst

Данное событие используется для установки значения временного интервала, после которого будет происходит
самообновление (autorefresh) списка. Установленное значение сразу вступает в силу.

Вызывается из шаблона
---------------------

Данное событие вызывается в JavaScript функции ``set_refresh_interval`` при изменении значения в подразделе
"Перезагрузка" раздела "Столбцы" на стандартной панели списка K4.

Потенциальное применение
------------------------

Данное событие событие может быть использовано для сохранения в базу (в таблицу
:doc:`/database/table_structure/persistant_session_data`) значения переменной: ``<prefix_special>_refresh_interval``.

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnSetAutoRefreshInterval
