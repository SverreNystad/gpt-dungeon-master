from knowledge_base.rag_service import lookup_rules

def test_no_context_given_should_return_empty_list():
    # Arrange
    context = [Context()]

    # Act
    rules =  lookup_rules(context)

    # Assert
    assert rules == []


def test_ability_saving_throw_should_return_rules():
    # Arrange
    context = [Context(ability_saving_throw=AbilitySavingThrow.STRENGTH)]

    # Act
    rules =  lookup_rules(context)

    # Assert
    assert rules == [Rule(ability_saving_throw=AbilitySavingThrow.STRENGTH)]