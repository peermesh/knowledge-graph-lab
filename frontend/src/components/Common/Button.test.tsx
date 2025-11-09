import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button Component', () => {
  describe('Rendering', () => {
    it('renders with default props', () => {
      render(<Button>Click me</Button>)
      const button = screen.getByRole('button', { name: /click me/i })
      expect(button).toBeInTheDocument()
      expect(button).toHaveTextContent('Click me')
    })

    it('renders with custom children', () => {
      render(
        <Button>
          <span>Custom</span> Content
        </Button>
      )
      expect(screen.getByText('Custom')).toBeInTheDocument()
      expect(screen.getByText('Content')).toBeInTheDocument()
    })

    it('renders with icon', () => {
      render(
        <Button>
          <svg data-testid="icon" />
          Text
        </Button>
      )
      expect(screen.getByTestId('icon')).toBeInTheDocument()
      expect(screen.getByText('Text')).toBeInTheDocument()
    })
  })

  describe('Variants', () => {
    it('renders default variant', () => {
      render(<Button variant="default">Default</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('bg-primary')
    })

    it('renders destructive variant', () => {
      render(<Button variant="destructive">Delete</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('bg-destructive')
    })

    it('renders outline variant', () => {
      render(<Button variant="outline">Outline</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('border')
    })

    it('renders secondary variant', () => {
      render(<Button variant="secondary">Secondary</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('bg-secondary')
    })

    it('renders ghost variant', () => {
      render(<Button variant="ghost">Ghost</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('hover:bg-accent')
    })

    it('renders link variant', () => {
      render(<Button variant="link">Link</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('underline-offset-4')
    })
  })

  describe('Sizes', () => {
    it('renders default size', () => {
      render(<Button size="default">Default Size</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('h-10')
    })

    it('renders small size', () => {
      render(<Button size="sm">Small</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('h-9')
    })

    it('renders large size', () => {
      render(<Button size="lg">Large</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('h-11')
    })

    it('renders icon size', () => {
      render(<Button size="icon">Icon</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('h-10', 'w-10')
    })
  })

  describe('States', () => {
    it('handles disabled state', () => {
      render(<Button disabled>Disabled</Button>)
      const button = screen.getByRole('button')
      expect(button).toBeDisabled()
      expect(button).toHaveClass('disabled:opacity-50')
    })

    it('does not call onClick when disabled', () => {
      const handleClick = vi.fn()
      render(<Button disabled onClick={handleClick}>Disabled</Button>)
      const button = screen.getByRole('button')
      
      fireEvent.click(button)
      expect(handleClick).not.toHaveBeenCalled()
    })
  })

  describe('Interactions', () => {
    it('calls onClick when clicked', () => {
      const handleClick = vi.fn()
      render(<Button onClick={handleClick}>Click me</Button>)
      
      const button = screen.getByRole('button')
      fireEvent.click(button)
      
      expect(handleClick).toHaveBeenCalledTimes(1)
    })

    it('calls onClick multiple times', () => {
      const handleClick = vi.fn()
      render(<Button onClick={handleClick}>Click me</Button>)
      
      const button = screen.getByRole('button')
      fireEvent.click(button)
      fireEvent.click(button)
      fireEvent.click(button)
      
      expect(handleClick).toHaveBeenCalledTimes(3)
    })

    it('receives click event object', () => {
      const handleClick = vi.fn()
      render(<Button onClick={handleClick}>Click me</Button>)
      
      const button = screen.getByRole('button')
      fireEvent.click(button)
      
      expect(handleClick).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'click',
        })
      )
    })
  })

  describe('Props', () => {
    it('forwards type prop', () => {
      render(<Button type="submit">Submit</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveAttribute('type', 'submit')
    })

    it('forwards className prop', () => {
      render(<Button className="custom-class">Custom</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveClass('custom-class')
    })

    it('forwards data attributes', () => {
      render(<Button data-testid="my-button" data-custom="value">Test</Button>)
      const button = screen.getByTestId('my-button')
      expect(button).toHaveAttribute('data-custom', 'value')
    })

    it('forwards aria attributes', () => {
      render(<Button aria-label="Close dialog">X</Button>)
      const button = screen.getByRole('button', { name: /close dialog/i })
      expect(button).toHaveAttribute('aria-label', 'Close dialog')
    })
  })

  describe('Accessibility', () => {
    it('is keyboard accessible', () => {
      const handleClick = vi.fn()
      render(<Button onClick={handleClick}>Click me</Button>)
      
      const button = screen.getByRole('button')
      button.focus()
      
      fireEvent.keyDown(button, { key: 'Enter' })
      // Note: fireEvent doesn't trigger click on Enter by default
      // This tests that the button is focusable
      expect(button).toHaveFocus()
    })

    it('has proper role', () => {
      render(<Button>Button</Button>)
      const button = screen.getByRole('button')
      expect(button).toBeInTheDocument()
    })

    it('respects aria-disabled', () => {
      render(<Button aria-disabled="true">Disabled</Button>)
      const button = screen.getByRole('button')
      expect(button).toHaveAttribute('aria-disabled', 'true')
    })
  })

  describe('Edge Cases', () => {
    it('handles empty children', () => {
      render(<Button>{''}</Button>)
      const button = screen.getByRole('button')
      expect(button).toBeInTheDocument()
      expect(button).toHaveTextContent('')
    })

    it('handles null children gracefully', () => {
      render(<Button>{null}</Button>)
      const button = screen.getByRole('button')
      expect(button).toBeInTheDocument()
    })

    it('combines multiple variants/sizes with className', () => {
      render(
        <Button
          variant="destructive"
          size="lg"
          className="custom-spacing"
        >
          Combined
        </Button>
      )
      const button = screen.getByRole('button')
      expect(button).toHaveClass('bg-destructive', 'h-11', 'custom-spacing')
    })
  })

  describe('Refs', () => {
    it('forwards ref to button element', () => {
      const ref = vi.fn()
      render(<Button ref={ref}>Button</Button>)
      
      expect(ref).toHaveBeenCalled()
      const buttonElement = ref.mock.calls[0][0]
      expect(buttonElement).toBeInstanceOf(HTMLButtonElement)
    })

    it('can access button methods through ref', () => {
      let buttonRef: HTMLButtonElement | null = null
      render(
        <Button ref={(el) => { buttonRef = el }}>
          Button
        </Button>
      )
      
      expect(buttonRef).not.toBeNull()
      expect(buttonRef?.tagName).toBe('BUTTON')
    })
  })
})



