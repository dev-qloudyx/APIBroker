if (kendo.ui.DateTimePicker) {
  kendo.ui.DateTimePicker.prototype.options.messages =
    $.extend(true, kendo.ui.DateTimePicker.prototype.options.messages, {
      "date": "Data",
      "time": "Horas",
      "today": "Hoje",
      "set": "Guardar",
      "cancel": "Cancelar",
      "hour": "Hora",
      "minute": "Minuto",
      "now": "Agora"
    });
}
if (kendo.ui.Calendar) {
  kendo.ui.Calendar.prototype.options.messages =
    $.extend(true, kendo.ui.Calendar.prototype.options.messages, {
      "today": "Hoje"
    });
}
if (kendo.ui.Scheduler) {
  kendo.ui.Scheduler.prototype.options.messages =
    $.extend(true, kendo.ui.Scheduler.prototype.options.messages, {
      "time": "Processo | Matricula"
    });
}
kendo.culture("pt-PT");