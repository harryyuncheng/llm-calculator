#!/usr/bin/env python3
"""
LLM-Backed Calculator GUI Application

A simple calculator that uses Claude API to perform calculations.
The GUI displays button input as a string expression and sends it to Claude for evaluation.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import re
import os


class LLMCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("LLM Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Load environment variables
        self.load_env_variables()
        
        # Current expression being built
        self.current_expression = ""
        
        # Track all buttons for disabling/enabling
        self.all_buttons = []
        
        # Create the display
        self.create_display()
        
        # Create the buttons
        self.create_buttons()
        
        # Set initial focus to expression field
        self.expression_display.focus_set()
    
    def load_env_variables(self):
        """Load environment variables for API configuration"""
        try:
            # Try to load from .env file
            if os.path.exists('.env'):
                with open('.env', 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            os.environ[key] = value
        except Exception as e:
            print(f"Note: Could not load .env file: {e}")
        
        # Set default values
        self.api_key = os.getenv('ANTHROPIC_API_KEY', '')
        self.claude_model = 'claude-3-haiku-20240307'
        self.max_tokens = 1024
        self.timeout = 30
    
    def create_display(self):
        """Create the display area for showing the current expression and result"""
        # Frame for display
        display_frame = tk.Frame(self.root, bg='lightgray', padx=5, pady=5)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Expression display (what user is typing)
        tk.Label(display_frame, text="Expression:", bg='lightgray', anchor='w').pack(fill=tk.X)
        self.expression_var = tk.StringVar()
        self.expression_display = tk.Entry(
            display_frame, 
            textvariable=self.expression_var, 
            font=('Arial', 12), 
            justify='right'
        )
        # Bind keyboard input validation
        self.expression_display.bind('<KeyPress>', self.validate_key_input)
        self.expression_display.bind('<KeyRelease>', self.on_text_change)
        self.expression_display.pack(fill=tk.X, pady=(0, 10))
        
        # Result display
        tk.Label(display_frame, text="Result:", bg='lightgray', anchor='w').pack(fill=tk.X)
        self.result_var = tk.StringVar()
        self.result_display = tk.Entry(
            display_frame, 
            textvariable=self.result_var, 
            font=('Arial', 14, 'bold'), 
            state='readonly',
            justify='right',
            bg='white'
        )
        self.result_display.pack(fill=tk.X)
    
    def create_buttons(self):
        """Create all calculator buttons"""
        # Main button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button configuration
        button_config = {
            'font': ('Arial', 12),
            'width': 5,
            'height': 2,
            'relief': 'raised',  # Raised button appearance
            'borderwidth': 2,    # Clear border
            'activebackground': 'lightgray',  # Visual feedback when pressed
            'activeforeground': 'black'       # Text color when pressed
        }
        
        # Row 1: Clear and Close buttons
        clear_btn = tk.Button(
            button_frame, text="Clear", bg='orange', 
            command=self.clear_display, **button_config
        )
        clear_btn.grid(row=0, column=0, columnspan=2, sticky='ew', padx=3, pady=3)
        self.all_buttons.append(clear_btn)
        
        close_btn = tk.Button(
            button_frame, text="Close", bg='red', fg='black',
            command=self.close_app, **button_config
        )
        close_btn.grid(row=0, column=2, columnspan=2, sticky='ew', padx=3, pady=3)
        # Don't add Close button to disabled list - should always work
        
        # Row 2: 7, 8, 9, /
        self.create_button(button_frame, "7", 1, 0, **button_config)
        self.create_button(button_frame, "8", 1, 1, **button_config)
        self.create_button(button_frame, "9", 1, 2, **button_config)
        self.create_button(button_frame, "/", 1, 3, bg='lightblue', **button_config)
        
        # Row 3: 4, 5, 6, *
        self.create_button(button_frame, "4", 2, 0, **button_config)
        self.create_button(button_frame, "5", 2, 1, **button_config)
        self.create_button(button_frame, "6", 2, 2, **button_config)
        self.create_button(button_frame, "*", 2, 3, bg='lightblue', **button_config)
        
        # Row 4: 1, 2, 3, -
        self.create_button(button_frame, "1", 3, 0, **button_config)
        self.create_button(button_frame, "2", 3, 1, **button_config)
        self.create_button(button_frame, "3", 3, 2, **button_config)
        self.create_button(button_frame, "-", 3, 3, bg='lightblue', **button_config)
        
        # Row 5: 0, ., +, =
        self.create_button(button_frame, "0", 4, 0, **button_config)
        self.create_button(button_frame, ".", 4, 1, **button_config)
        self.create_button(button_frame, "+", 4, 2, bg='lightblue', **button_config)
        self.create_button(button_frame, "=", 4, 3, bg='green', fg='black', **button_config)
        
        # Configure grid weights for responsive layout
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)
    
    def create_button(self, parent, text, row, col, **kwargs):
        """Helper method to create a button with click handler"""
        if text == "=":
            command = self.calculate_result
        else:
            command = lambda t=text: self.button_click(t)
        
        btn = tk.Button(parent, text=text, command=command, **kwargs)
        btn.grid(row=row, column=col, sticky='ew', padx=3, pady=3)  # Increased padding
        
        # Add to button list for disabling (except Close button)
        if text != "Close":
            self.all_buttons.append(btn)
        
        return btn
    
    def button_click(self, value):
        """Handle button clicks for digits and operators"""
        # Add the clicked value to current expression
        self.current_expression += str(value)
        self.update_display()
        # Focus the entry field so user can continue typing
        self.expression_display.focus_set()
        # Move cursor to end
        self.expression_display.icursor(tk.END)
    
    def update_display(self):
        """Update the expression display"""
        self.expression_var.set(self.current_expression)
    
    def clear_display(self):
        """Clear the display and reset current expression"""
        self.current_expression = ""
        self.expression_var.set("")
        self.result_var.set("")
        # Focus the entry field for immediate typing
        self.expression_display.focus_set()
        # No need to enable buttons here - they should already be enabled
    
    def close_app(self):
        """Close the application"""
        self.root.quit()
        sys.exit(0)
    
    def calculate_result(self):
        """Send current expression to Claude API for calculation"""
        if not self.current_expression.strip():
            messagebox.showwarning("Warning", "Please enter an expression first!")
            return
        
        # Disable all buttons while waiting for Claude response
        self.disable_buttons()
        
        try:
            # Create prompt for Claude
            prompt = f"What is the result of this calculation: {self.current_expression}?"
            
            # Call Claude API (placeholder implementation)
            result = self.query_claude(prompt)
            
            # Display the result
            self.result_var.set(str(result))
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {str(e)}")
            self.result_var.set("Error")
        finally:
            # Always re-enable buttons after getting response (success or failure)
            self.enable_buttons()
    
    def query_claude(self, prompt):
        """
        Claude API integration with fallback to simulation.
        
        If ANTHROPIC_API_KEY is set in environment, uses real Claude API.
        Otherwise, falls back to simulation for demonstration.
        """
        print(f"Sending to Claude API: {prompt}")
        
        # Try real API first if API key is available
        if self.api_key:
            try:
                result = self.query_claude_real(prompt)
                return result
            except Exception as e:
                print(f"Real API failed, falling back to simulation: {e}")
                # Fall through to simulation
        
        # Simulate API delay
        self.root.update()
        self.root.after(500)  # 500ms delay to simulate API call
        
        # Simulation mode for demonstration
        try:
            # Extract just the mathematical expression from our stored expression
            expression = self.current_expression.strip()
            
            # Simulate Claude's response format
            simulated_response = f"The result of {expression} is {eval(expression)}."
            print(f"Claude API simulation response: {simulated_response}")
            
            # Extract numerical result from response
            result = eval(expression)  # In real implementation, parse from Claude's text response
            
            return result
            
        except Exception as e:
            raise Exception(f"Calculation failed: {str(e)}")
    
    # TODO: Implement real Claude API integration
    def query_claude_real(self, prompt):
        """
        Real Claude API integration template.
        This will be used when you have a valid API key in your .env file.
        """
        if not self.api_key:
            raise Exception("ANTHROPIC_API_KEY not found in environment variables. Please add it to your .env file.")
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(
                api_key=self.api_key
            )
            
            message = client.messages.create(
                model=self.claude_model,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text
            print(f"Claude API response: {response_text}")
            
            # Extract numerical result from Claude's response
            # Look for numbers in the response, preferring the last one found
            numbers = re.findall(r'-?\d+\.?\d*', response_text)
            if numbers:
                return float(numbers[-1])  # Return last number found
            else:
                # Try to find words like "equals", "is", "result" followed by numbers
                result_patterns = [
                    r'(?:equals?|is|result|answer)\s*:?\s*(-?\d+\.?\d*)',
                    r'(-?\d+\.?\d*)\s*$',  # Number at end of response
                ]
                for pattern in result_patterns:
                    match = re.search(pattern, response_text, re.IGNORECASE)
                    if match:
                        return float(match.group(1))
                
                raise Exception("Could not parse numerical result from Claude's response")
                
        except ImportError:
            raise Exception("anthropic library not installed. Run: pip install anthropic")
        except Exception as e:
            raise Exception(f"Claude API call failed: {str(e)}")
    
    def disable_buttons(self):
        """Disable all buttons and change their appearance to indicate disabled state"""
        for button in self.all_buttons:
            button.config(
                state='disabled',
                bg='gray',  # Gray background for disabled state
                fg='darkgray',  # Darker gray text
                cursor='arrow'  # Change cursor back to arrow
            )
        
        # Also disable the expression field to prevent typing
        self.expression_display.config(state='readonly')
    
    def enable_buttons(self):
        """Re-enable all buttons and restore their original appearance"""
        for button in self.all_buttons:
            # Get the button text to determine original colors
            button_text = button.cget('text')
            
            # Restore original colors based on button type
            if button_text == "Clear":
                bg_color = 'orange'
            elif button_text in ['+', '-', '*', '/']:
                bg_color = 'lightblue'
            elif button_text == '=':
                bg_color = 'green'
            else:
                bg_color = 'SystemButtonFace'  # Default button color
            
            # Restore button appearance
            button.config(
                state='normal',
                bg=bg_color,
                fg='black',
                cursor='hand2'
            )
        
        # Re-enable the expression field
        self.expression_display.config(state='normal')
    
    def validate_key_input(self, event):
        """Validate keyboard input - only allow numbers, operators, and specific keys"""
        # Allow these characters: digits, operators, decimal point, backspace, delete, arrow keys
        allowed_chars = '0123456789+-*/.='
        
        # Allow control keys (backspace, delete, arrow keys, etc.)
        if event.keysym in ['BackSpace', 'Delete', 'Left', 'Right', 'Home', 'End', 'Tab']:
            return True
        
        # Allow Enter key to trigger calculation
        if event.keysym == 'Return':
            self.calculate_result()
            return "break"  # Prevent default behavior
        
        # Check if the character is allowed
        if event.char in allowed_chars:
            return True
        
        # Block all other characters (letters, symbols, etc.)
        return "break"  # Prevent the key from being processed
    
    def on_text_change(self, event):
        """Handle text changes in the expression field"""
        # Update our internal expression variable
        self.current_expression = self.expression_var.get()
    


def main():
    """Main function to run the calculator"""
    root = tk.Tk()
    calculator = LLMCalculator(root)
    
    # Center the window on screen
    root.eval('tk::PlaceWindow . center')
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
