import pytest

def test_addition():
    """Test basic addition"""
    result = 2 + 2
    assert result == 4
    print("✓ Addition test passed successfully!")

def test_subtraction():
    """Test basic subtraction"""
    result = 10 - 5
    assert result == 5
    print("✓ Subtraction test passed successfully!")

def test_multiplication():
    """Test basic multiplication"""
    result = 3 * 4
    assert result == 12
    print("✓ Multiplication test passed successfully!")

def test_string_length():
    """Test string operations"""
    message = "Hello Jenkins"
    assert len(message) == 13
    print("✓ String length test passed successfully!")

def test_list_operations():
    """Test list operations"""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert numbers[0] == 1
    print("✓ List operations test passed successfully!")

def test_final_message():
    """Final success message"""
    print("\n ALL TESTS RAN SUCCESSFULLY!")
    print("Jenkins pipeline testing completed!")
    assert True