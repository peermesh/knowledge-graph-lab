import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Input } from './Input'

describe('Input Component', () => {
  describe('Rendering', () => {
    it('renders correctly', () => {
      render(<Input placeholder="Enter text" />)
      const input = screen.getByPlaceholderText('Enter text')
      expect(input).toBeInTheDocument()
    })

    it('renders with default type', () => {
      render(<Input />)
      const input = screen.getByRole('textbox')
      expect(input).toHaveAttribute('type', 'text')
    })

    it('renders with custom type', () => {
      render(<Input type="email" />)
      const input = screen.getByRole('textbox')
      expect(input).toHaveAttribute('type', 'email')
    })

    it('renders password input', () => {
      render(<Input type="password" />)
      const inputs = document.querySelectorAll('input[type="password"]')
      expect(inputs).toHaveLength(1)
    })
  })

  describe('Value Management', () => {
    it('handles controlled input', () => {
      const { rerender } = render(<Input value="initial" onChange={() => {}} />)
      const input = screen.getByRole('textbox') as HTMLInputElement
      expect(input.value).toBe('initial')

      rerender(<Input value="updated" onChange={() => {}} />)
      expect(input.value).toBe('updated')
    })

    it('handles uncontrolled input', () => {
      render(<Input defaultValue="default" />)
      const input = screen.getByRole('textbox') as HTMLInputElement
      expect(input.value).toBe('default')
    })

    it('updates value on user input', async () => {
      const user = userEvent.setup()
      render(<Input />)
      const input = screen.getByRole('textbox') as HTMLInputElement

      await user.type(input, 'Hello')
      expect(input.value).toBe('Hello')
    })

    it('clears value when empty string provided', () => {
      const { rerender } = render(<Input value="text" onChange={() => {}} />)
      const input = screen.getByRole('textbox') as HTMLInputElement
      expect(input.value).toBe('text')

      rerender(<Input value="" onChange={() => {}} />)
      expect(input.value).toBe('')
    })
  })

  describe('Interactions', () => {
    it('calls onChange when typing', async () => {
      const handleChange = vi.fn()
      const user = userEvent.setup()
      render(<Input onChange={handleChange} />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'a')
      
      expect(handleChange).toHaveBeenCalled()
    })

    it('calls onChange with event object', () => {
      const handleChange = vi.fn()
      render(<Input onChange={handleChange} />)
      
      const input = screen.getByRole('textbox')
      fireEvent.change(input, { target: { value: 'test' } })
      
      expect(handleChange).toHaveBeenCalledWith(
        expect.objectContaining({
          target: expect.objectContaining({
            value: 'test'
          })
        })
      )
    })

    it('calls onFocus when focused', () => {
      const handleFocus = vi.fn()
      render(<Input onFocus={handleFocus} />)
      
      const input = screen.getByRole('textbox')
      input.focus()
      
      expect(handleFocus).toHaveBeenCalledTimes(1)
    })

    it('calls onBlur when blurred', () => {
      const handleBlur = vi.fn()
      render(<Input onBlur={handleBlur} />)
      
      const input = screen.getByRole('textbox')
      input.focus()
      input.blur()
      
      expect(handleBlur).toHaveBeenCalledTimes(1)
    })

    it('calls onKeyDown when key pressed', () => {
      const handleKeyDown = vi.fn()
      render(<Input onKeyDown={handleKeyDown} />)
      
      const input = screen.getByRole('textbox')
      fireEvent.keyDown(input, { key: 'Enter' })
      
      expect(handleKeyDown).toHaveBeenCalled()
    })
  })

  describe('Props', () => {
    it('forwards className prop', () => {
      render(<Input className="custom-class" />)
      const input = screen.getByRole('textbox')
      expect(input).toHaveClass('custom-class')
    })

    it('forwards placeholder prop', () => {
      render(<Input placeholder="Type here..." />)
      const input = screen.getByPlaceholderText('Type here...')
      expect(input).toBeInTheDocument()
    })

    it('forwards name prop', () => {
      render(<Input name="email" />)
      const input = screen.getByRole('textbox')
      expect(input).toHaveAttribute('name', 'email')
    })

    it('forwards id prop', () => {
      render(<Input id="my-input" />)
      const input = screen.getByRole('textbox')
      expect(input).toHaveAttribute('id', 'my-input')
    })

    it('forwards data attributes', () => {
      render(<Input data-testid="custom-input" data-custom="value" />)
      const input = screen.getByTestId('custom-input')
      expect(input).toHaveAttribute('data-custom', 'value')
    })

    it('forwards aria attributes', () => {
      render(<Input aria-label="Email input" aria-required="true" />)
      const input = screen.getByLabelText('Email input')
      expect(input).toHaveAttribute('aria-required', 'true')
    })
  })

  describe('States', () => {
    it('handles disabled state', () => {
      render(<Input disabled />)
      const input = screen.getByRole('textbox')
      expect(input).toBeDisabled()
      expect(input).toHaveClass('disabled:opacity-50')
    })

    it('does not accept input when disabled', async () => {
      const user = userEvent.setup()
      render(<Input disabled />)
      const input = screen.getByRole('textbox') as HTMLInputElement

      await user.type(input, 'test')
      expect(input.value).toBe('')
    })

    it('handles readonly state', () => {
      render(<Input readOnly value="readonly" />)
      const input = screen.getByRole('textbox') as HTMLInputElement
      expect(input).toHaveAttribute('readonly')
      expect(input.value).toBe('readonly')
    })

    it('handles required state', () => {
      render(<Input required />)
      const input = screen.getByRole('textbox')
      expect(input).toBeRequired()
    })
  })

  describe('Input Types', () => {
    it('accepts text input', async () => {
      const user = userEvent.setup()
      render(<Input type="text" />)
      const input = screen.getByRole('textbox') as HTMLInputElement

      await user.type(input, 'Hello World')
      expect(input.value).toBe('Hello World')
    })

    it('accepts email input', () => {
      render(<Input type="email" />)
      const input = screen.getByRole('textbox')
      expect(input).toHaveAttribute('type', 'email')
    })

    it('accepts number input', () => {
      render(<Input type="number" />)
      const input = document.querySelector('input[type="number"]')
      expect(input).toBeInTheDocument()
    })

    it('accepts password input', () => {
      render(<Input type="password" />)
      const input = document.querySelector('input[type="password"]')
      expect(input).toBeInTheDocument()
    })

    it('accepts search input', () => {
      render(<Input type="search" />)
      const input = screen.getByRole('searchbox')
      expect(input).toBeInTheDocument()
    })
  })

  describe('Form Integration', () => {
    it('works within a form', () => {
      const handleSubmit = vi.fn((e) => e.preventDefault())
      render(
        <form onSubmit={handleSubmit}>
          <Input name="username" />
          <button type="submit">Submit</button>
        </form>
      )

      const button = screen.getByRole('button', { name: /submit/i })
      fireEvent.click(button)

      expect(handleSubmit).toHaveBeenCalled()
    })

    it('includes value in form data', () => {
      render(
        <form>
          <Input name="email" defaultValue="test@example.com" />
        </form>
      )

      const input = screen.getByRole('textbox') as HTMLInputElement
      expect(input.name).toBe('email')
      expect(input.value).toBe('test@example.com')
    })
  })

  describe('Accessibility', () => {
    it('is keyboard accessible', () => {
      render(<Input />)
      const input = screen.getByRole('textbox')
      
      input.focus()
      expect(input).toHaveFocus()
    })

    it('supports aria-label', () => {
      render(<Input aria-label="Search input" />)
      const input = screen.getByLabelText('Search input')
      expect(input).toBeInTheDocument()
    })

    it('supports aria-describedby', () => {
      render(
        <>
          <Input aria-describedby="helper-text" />
          <span id="helper-text">Helper text</span>
        </>
      )
      const input = screen.getByRole('textbox')
      expect(input).toHaveAttribute('aria-describedby', 'helper-text')
    })

    it('supports aria-invalid', () => {
      render(<Input aria-invalid="true" />)
      const input = screen.getByRole('textbox')
      expect(input).toHaveAttribute('aria-invalid', 'true')
    })
  })

  describe('Refs', () => {
    it('forwards ref to input element', () => {
      const ref = vi.fn()
      render(<Input ref={ref} />)
      
      expect(ref).toHaveBeenCalled()
      const inputElement = ref.mock.calls[0][0]
      expect(inputElement).toBeInstanceOf(HTMLInputElement)
    })

    it('can access input methods through ref', () => {
      let inputRef: HTMLInputElement | null = null
      render(
        <Input ref={(el) => { inputRef = el }} />
      )
      
      expect(inputRef).not.toBeNull()
      expect(inputRef?.tagName).toBe('INPUT')
      expect(inputRef?.focus).toBeInstanceOf(Function)
    })

    it('can focus input through ref', () => {
      let inputRef: HTMLInputElement | null = null
      render(
        <Input ref={(el) => { inputRef = el }} />
      )
      
      inputRef?.focus()
      expect(inputRef).toHaveFocus()
    })
  })

  describe('Edge Cases', () => {
    it('handles rapid value changes', () => {
      const { rerender } = render(<Input value="a" onChange={() => {}} />)
      const input = screen.getByRole('textbox') as HTMLInputElement

      expect(input.value).toBe('a')
      rerender(<Input value="ab" onChange={() => {}} />)
      expect(input.value).toBe('ab')
      rerender(<Input value="abc" onChange={() => {}} />)
      expect(input.value).toBe('abc')
    })

    it('handles special characters', async () => {
      const user = userEvent.setup()
      render(<Input />)
      const input = screen.getByRole('textbox') as HTMLInputElement

      await user.type(input, '!@#$%^&*()')
      expect(input.value).toBe('!@#$%^&*()')
    })

    it('handles unicode characters', async () => {
      const user = userEvent.setup()
      render(<Input />)
      const input = screen.getByRole('textbox') as HTMLInputElement

      await user.type(input, '你好世界')
      expect(input.value).toBe('你好世界')
    })

    it('handles very long input', async () => {
      const user = userEvent.setup()
      const longText = 'a'.repeat(1000)
      render(<Input />)
      const input = screen.getByRole('textbox') as HTMLInputElement

      fireEvent.change(input, { target: { value: longText } })
      expect(input.value).toBe(longText)
    })
  })
})

