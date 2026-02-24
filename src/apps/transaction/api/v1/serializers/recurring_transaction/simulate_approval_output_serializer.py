from django.utils import timezone
from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import RecurringTransactionModel


class SimulateApprovalOutputSerializer(serializers.ModelSerializer):
    account = BaseMiniSerializer({
        "id": serializers.UUIDField(),
        "name": serializers.CharField()
    })
    anticipation_preview = serializers.SerializerMethodField()

    class Meta:
        model = RecurringTransactionModel
        fields = [
            'id',
            'value',
            'type_transaction',
            'description',
            'frequency',
            'account',
            'anticipation_preview',
        ]

    def get_execution_date_preview(self, obj: RecurringTransactionModel):
        return self.context.get('reference_date')

    def get_next_cycle_date_preview(self, obj: RecurringTransactionModel):
        return obj.calculate_next_date_from_base(self.get_execution_date_preview(obj))
    
    def get_anticipation_preview(self, obj: RecurringTransactionModel):
        exec_date = self.get_execution_date_preview(obj)
        target_date_local = timezone.localtime(obj.next_run_date)

        return {
            "target_scheduled_date": target_date_local, # o original (que seria executado sem alterações manuais)
            "execution_date": exec_date, # se fosse executado agora seria esse horário
            "next_scheduled_date": self.get_next_cycle_date_preview(obj) # após ser executado agora, a nova data para executar será essa
        }
