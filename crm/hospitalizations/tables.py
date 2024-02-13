from hospitalizations import converters
from tables import buttons, fields, schemas
from tables.html import HTMLAttributes


class CurrentHospitalizationsTable(schemas.TableSchema):
    patient = fields.TextLinkSortedField(
        verbose_name="ФИО",
        view_name_th="hospitalizations:current",
        attrs_th=HTMLAttributes(attrs={"style": "width: 30%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle ps-2"}),
        view_name_td="hospitalizations:hospitalizations",
        converters=(converters.FioConverter(),),
    )
    entry_date = fields.TextSortedField(
        verbose_name="Дата поступления",
        view_name_th="hospitalizations:current",
        attrs_th=HTMLAttributes(attrs={"style": "width: 20%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle text-center"}),
    )
    notes = fields.TextField(
        verbose_name="Заметки",
        attrs_th=HTMLAttributes(attrs={"style": "width: 20%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle text-center"}),
    )
    actions = fields.ButtonsField(
        verbose_name="Действия",
        buttons=[
            buttons.LeaveButton(
                name="Выписать", view_name="hospitalizations:leave"
            ),
            buttons.UpdateButton(
                name="Изменить", view_name="hospitalizations:update_current"
            ),
            buttons.DeleteButton(
                name="Удалить", view_name="hospitalizations:delete_current"
            ),
        ],
        attrs_td=HTMLAttributes(attrs={"class": "align-middle text-center"}),
    )

    class Meta:
        index = ["patient", "entry_date", "notes", "actions"]


class HospitalizationsTable(schemas.TableSchema):
    entry_date = fields.TextSortedField(
        verbose_name="Дата поступления",
        view_name_th="hospitalizations:hospitalizations",
        attrs_th=HTMLAttributes(attrs={"style": "width: 20%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle text-center"}),
    )
    leaving_date = fields.TextSortedField(
        verbose_name="Дата выписки",
        view_name_th="hospitalizations:hospitalizations",
        attrs_th=HTMLAttributes(attrs={"style": "width: 20%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle text-center"}),
        default="находится на лечении",
    )
    notes = fields.TextSortedField(
        verbose_name="Заметки",
        attrs_th=HTMLAttributes(attrs={"style": "width: 30%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle ps-2"}),
    )
    actions = fields.ButtonsField(
        verbose_name="Действия",
        buttons=[
            buttons.UpdateInlineButton(
                name="Изменить", view_name="hospitalizations:update"
            ),
            buttons.DeleteButton(
                name="Удалить", view_name="hospitalizations:delete"
            ),
        ],
        attrs_th=HTMLAttributes(attrs={"style": "width: 20%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle text-center"}),
    )

    class Meta:
        index = ("entry_date", "leaving_date", "notes", "actions")
