import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import BookCard from '../components/BookCard'

describe('BookCard', () => {
  const mockBook = {
    title: '沙丘',
    author: '弗兰克·赫伯特',
    isbn: '978-7-5321-5614-4',
    summary: '沙漠星球上的权力斗争与人类进化的史诗',
    recommendation_reason: '宏大的世界观和深刻的哲学思考',
  }

  it('should render book information', () => {
    render(<BookCard book={mockBook} rank={1} />)

    expect(screen.getByText('沙丘')).toBeInTheDocument()
    expect(screen.getByText('作者：弗兰克·赫伯特')).toBeInTheDocument()
    expect(screen.getByText(/ISBN: 978-7-5321-5614-4/)).toBeInTheDocument()
  })

  it('should display rank number', () => {
    render(<BookCard book={mockBook} rank={2} />)

    expect(screen.getByText('#2')).toBeInTheDocument()
  })

  it('should render summary and recommendation reason', () => {
    render(<BookCard book={mockBook} rank={1} />)

    expect(
      screen.getByText('沙漠星球上的权力斗争与人类进化的史诗')
    ).toBeInTheDocument()
    expect(
      screen.getByText('宏大的世界观和深刻的哲学思考')
    ).toBeInTheDocument()
  })

  it('should render action buttons', () => {
    render(<BookCard book={mockBook} rank={1} />)

    expect(screen.getByText('我想读这本')).toBeInTheDocument()
    expect(screen.getByText('了解更多')).toBeInTheDocument()
  })
})
