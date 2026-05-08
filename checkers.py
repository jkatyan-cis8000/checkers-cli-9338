#!/usr/bin/env python3
"""Checkers (Draughts) CLI game."""

class CheckersGame:
    def __init__(self):
        self.board = self._initialize_board()
        self.current_player = 'red'
        self.game_over = False
        self.must_jump_from = None

    def _initialize_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        board[row][col] = {'player': 'black', 'king': False}
                    elif row > 4:
                        board[row][col] = {'player': 'red', 'king': False}
        return board

    def board_to_string(self):
        lines = []
        lines.append("  0 1 2 3 4 5 6 7")
        for row in range(8):
            line = f"{row} "
            for col in range(8):
                if (row + col) % 2 == 0:
                    line += " _"
                else:
                    piece = self.board[row][col]
                    if piece is None:
                        line += " ."
                    elif piece['player'] == 'red':
                        line += " R" if not piece['king'] else " RR"
                    else:
                        line += " B" if not piece['king'] else " BB"
            lines.append(line)
        return "\n".join(lines)

    def display_board(self):
        print("\n" + self.board_to_string())

    def pos_to_coords(self, pos):
        if pos < 0 or pos > 63:
            return None
        row = pos // 8
        col = pos % 8
        if (row + col) % 2 == 0:
            return None
        return row, col

    def coords_to_pos(self, row, col):
        return row * 8 + col

    def get_valid_moves(self, row, col, piece):
        moves = []
        directions = []
        
        if piece['king']:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            if piece['player'] == 'red':
                directions = [(-1, -1), (-1, 1)]
            else:
                directions = [(1, -1), (1, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col] is None:
                    moves.append({
                        'from': self.coords_to_pos(row, col),
                        'to': self.coords_to_pos(new_row, new_col),
                        'jump': False
                    })
                elif self.board[new_row][new_col]['player'] != piece['player']:
                    jump_row, jump_col = new_row + dr, new_col + dc
                    if 0 <= jump_row < 8 and 0 <= jump_col < 8 and self.board[jump_row][jump_col] is None:
                        moves.append({
                            'from': self.coords_to_pos(row, col),
                            'to': self.coords_to_pos(jump_row, jump_col),
                            'jump': True,
                            'captured': self.coords_to_pos(new_row, new_col)
                        })
        
        return moves

    def get_all_moves(self, player):
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece['player'] == player:
                    moves = self.get_valid_moves(row, col, piece)
                    all_moves.extend(moves)
        return all_moves

    def get_jump_moves(self, player):
        all_moves = self.get_all_moves(player)
        return [m for m in all_moves if m['jump']]

    def make_move(self, from_pos, to_pos):
        from_row, from_col = self.pos_to_coords(from_pos)
        to_row, to_col = self.pos_to_coords(to_pos)
        
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece
        
        if piece['king']:
            return True
        
        if piece['player'] == 'red' and to_row == 0:
            piece['king'] = True
        elif piece['player'] == 'black' and to_row == 7:
            piece['king'] = True
        
        return True

    def handle_jump(self, from_pos, to_pos):
        from_row, from_col = self.pos_to_coords(from_pos)
        to_row, to_col = self.pos_to_coords(to_pos)
        
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        self.board[mid_row][mid_col] = None
        
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece
        
        if not piece['king']:
            if piece['player'] == 'red' and to_row == 0:
                piece['king'] = True
            elif piece['player'] == 'black' and to_row == 7:
                piece['king'] = True
        
        if piece['king']:
            return []
        
        additional_jumps = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            jump_row, jump_col = to_row + dr, to_col + dc
            if 0 <= jump_row < 8 and 0 <= jump_col < 8:
                if self.board[jump_row][jump_col] and self.board[jump_row][jump_col]['player'] != piece['player']:
                    landing_row, landing_col = jump_row + dr, jump_col + dc
                    if 0 <= landing_row < 8 and 0 <= landing_col < 8 and self.board[landing_row][landing_col] is None:
                        additional_jumps.append({
                            'from': self.coords_to_pos(to_row, to_col),
                            'to': self.coords_to_pos(landing_row, landing_col),
                            'jump': True,
                            'captured': self.coords_to_pos(jump_row, jump_col)
                        })
        
        return additional_jumps

    def parse_move(self, move_str):
        try:
            if '-' not in move_str:
                return None, "Invalid move format. Use 'from-to' (e.g., '3-7')"
            parts = move_str.split('-')
            if len(parts) != 2:
                return None, "Invalid move format. Use 'from-to' (e.g., '3-7')"
            from_pos = int(parts[0])
            to_pos = int(parts[1])
            if from_pos < 0 or from_pos > 63 or to_pos < 0 or to_pos > 63:
                return None, "Position out of range. Use 0-63."
            return from_pos, to_pos, None
        except ValueError:
            return None, None, "Invalid move format. Use 'from-to' (e.g., '3-7')"

    def is_valid_move(self, from_pos, to_pos):
        from_row, from_col = self.pos_to_coords(from_pos)
        to_row, to_col = self.pos_to_coords(to_pos)
        
        if from_row is None or to_row is None:
            return False, "Invalid starting or ending position."
        
        piece = self.board[from_row][from_col]
        if piece is None:
            return False, "No piece at starting position."
        if piece['player'] != self.current_player:
            return False, "That's not your piece."
        
        all_moves = self.get_valid_moves(from_row, from_col, piece)
        valid_move = None
        for move in all_moves:
            if move['to'] == to_pos:
                valid_move = move
                break
        
        if valid_move is None:
            return False, "Invalid move for that piece."
        
        if self.must_jump_from is not None and from_pos != self.must_jump_from:
            return False, "You must continue jumping with the same piece."
        
        return True, valid_move

    def check_win(self):
        red_count = 0
        black_count = 0
        for row in self.board:
            for piece in row:
                if piece:
                    if piece['player'] == 'red':
                        red_count += 1
                    else:
                        black_count += 1
        
        if red_count == 0:
            return 'black'
        elif black_count == 0:
            return 'red'
        return None

    def play(self):
        print("Checkers Game!")
        print("Board positions are numbered 0-63 (left to right, top to bottom)")
        print("Enter moves as 'from-to' (e.g., '3-7')")
        print("Red moves first.\n")
        
        while not self.game_over:
            self.display_board()
            
            all_jumps = self.get_jump_moves(self.current_player)
            if all_jumps and self.must_jump_from is None:
                print(f"\n{self.current_player.upper()} must jump!")
            
            move_str = input(f"\n{self.current_player.upper()}'s turn. Enter move: ").strip()
            
            if move_str.lower() in ['quit', 'q', 'exit']:
                print("Game ended.")
                break
            
            result = self.parse_move(move_str)
            if result is None or len(result) < 3:
                print("Invalid move format. Use 'from-to' (e.g., '3-7')")
                continue
            
            from_pos, to_pos, error = result
            if error:
                print(error)
                continue
            
            is_valid, move_info = self.is_valid_move(from_pos, to_pos)
            if not is_valid:
                print(move_info)
                continue
            
            if move_info['jump']:
                additional = self.handle_jump(from_pos, to_pos)
                if additional:
                    self.must_jump_from = to_pos
                    print("\n" + self.board_to_string())
                    print(f"\n{self.current_player.upper()} can make additional jumps!")
                    continue
                else:
                    self.must_jump_from = None
            else:
                if self.must_jump_from is not None:
                    print("You must continue jumping with the same piece.")
                    continue
                self.make_move(from_pos, to_pos)
            
            winner = self.check_win()
            if winner:
                self.display_board()
                print(f"\n{winner.upper()} wins!")
                self.game_over = True
                break
            
            self.current_player = 'black' if self.current_player == 'red' else 'red'
        
        print("Thanks for playing!")


if __name__ == "__main__":
    game = CheckersGame()
    game.play()
