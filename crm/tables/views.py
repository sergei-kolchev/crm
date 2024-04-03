class TableView:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.table_schema(
            view_name=getattr(self, "table_view_name", None),
            request_params=self.request.GET,
            request_kwargs=self.kwargs,
        )
        context["table"] = table.make_table(self.get_queryset())
        return context


class TableRowView:
    template_name = "tables/tr.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.table_schema(
            view_name=getattr(self, "table_view_name", None),
            request_params=self.request.GET,
            request_kwargs=self.kwargs,
        )
        context["object"] = table.get_body_row(self.get_queryset())
        return context


class TableInlineFormView:
    template_name = "tables/update_form_tr.html"
    context_object_name = "obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_view"] = self.table_row_update_view
        context["detail_view"] = self.table_row_detail_view
        return context
