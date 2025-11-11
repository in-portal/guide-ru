OnPreSaveAndOpenTranslator
==========================
`Data Source`_

.. include:: /includes/not_finished.rst

Событие вызывается при открытие окна переводчика (``Translator``) для мультиязычных полей. Сохраняет во временную
таблицу значение записи перед тем, как преступить к редактированию мультиязычного поля.

Вызывается из шаблона
---------------------

- in-edit\admin_templates\pages\pages_edit.tpl
- core\admin_templates\skins\skin_edit.tpl
- core\admin_templates\categories\categories_edit.tpl
- in-commerce\admin_templates\products\products_edit.tpl

Вызывается из событий
---------------------

Не вызывается из событий.

Вызывает события
----------------

- :doc:`/events/onpresave/on_pre_save`

Потенциальное применение
------------------------

На данный момент - только то, которое следует из описания.

Ограничения
-----------

Ограничений нет.

.. _Data Source: http://guide.in-portal.org/rus/index.php/EventHandler:OnPreSaveAndOpenTranslator
