#!/usr/bin/env python3
"""Test script for Checkers game."""
from checkers import CheckersGame

def test_initial_board():
    game = CheckersGame()
    board = game.board
    
    assert board[0][1]['player'] == 'black'
    assert board[0][3]['player'] == 'black'
    assert board[0][5]['player'] == 'black'
    assert board[0][7]['player'] == 'black'
    assert board[7][0]['player'] == 'red'
    assert board[7][2]['player'] == 'red'
    assert board[7][4]['player'] == 'red'
    assert board[7][6]['player'] == 'red'
    
    assert board[0][0] is None
    assert board[0][2] is None
    assert board[3][3] is None
    
    print("✓ test_initial_board passed")

def test_pos_conversion():
    game = CheckersGame()
    
    row, col = game.pos_to_coords(0)
    assert row == 0 and col == 0
    row, col = game.pos_to_coords(7)
    assert row == 0 and col == 7
    row, col = game.pos_to_coords(8)
    assert row == 1 and col == 0
    row, col = game.pos_to_coords(63)
    assert row == 7 and col == 7
    
    pos = game.coords_to_pos(0, 0)
    assert pos == 0
    pos = game.coords_to_pos(7, 7)
    assert pos == 63
    
    print("✓ test_pos_conversion passed")

def test_move_validation():
    game = CheckersGame()
    
    valid, result = game.is_valid_move(12, 16)
    assert valid == True
    assert result['jump'] == False
    
    valid, result = game.is_valid_move(0, 4)
    assert valid == False
    
    valid, result = game.is_valid_move(12, 20)
    assert valid == False
    
    print("✓ test_move_validation passed")

def test_capture():
    game = CheckersGame()
    game.board[3][3] = None
    game.board[2][4] = {'player': 'black', 'king': False}
    game.board[4][4] = {'player': 'red', 'king': False}
    
    valid, result = game.is_valid_move(5, 12)
    assert valid == False
    
    game.board[4][3] = {'player': 'black', 'king': False}
    game.board[5][2] = {'player': 'red', 'king': False}
    valid, result = game.is_valid_move(4, 11)
    assert valid == True
    assert result['jump'] == True
    assert result['captured'] == 14
    
    print("✓ test_capture passed")

def test_kinging():
    game = CheckersGame()
    game.board[1][0] = None
    game.board[0][1] = None
    game.board[6][7] = None
    game.board[7][6] = {'player': 'red', 'king': False}
    
    game.make_move(6, 7)
    
    piece = game.board[7][6]
    assert piece is not None
    assert piece['king'] == True
    
    game.board[1][6] = {'player': 'black', 'king': False}
    game.board[0][7] = None
    game.make_move(14, 7)
    piece = game.board[0][7]
    assert piece['king'] == True
    
    print("✓ test_kinging passed")

def test_display():
    game = CheckersGame()
    display = game.board_to_string()
    assert "R" in display
    assert "B" in display
    assert "0 1 2 3 4 5 6 7" in display
    assert " 0 " in display
    assert " 7 " in display
    
    print("✓ test_display passed")

if __name__ == "__main__":
    test_initial_board()
    test_pos_conversion()
    test_move_validation()
    test_capture()
    test_kinging()
    test_display()
    print("\n✓ All tests passed!")
