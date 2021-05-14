class MultiSerializerViewSetMixin(object):
    """Mixin для выбора нужного serializer"""
    def get_serializer_class(self):
        """Получить serializer для действия, заданного в serializer_action_classes"""
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
