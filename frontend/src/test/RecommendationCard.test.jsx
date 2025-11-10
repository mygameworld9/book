import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import RecommendationCard from '../components/RecommendationCard'

describe('RecommendationCard', () => {
  const mockItem = {
    title: '沙丘',
    creator: '弗兰克·赫伯特',
    metadata: {
      年份: '1965',
      类型: '科幻',
    },
    summary: '描绘厄拉科斯星球权力斗争与生态哲思的史诗级故事。',
    reason: '其宏大的世界观满足你对硬核科幻的期待。',
  }

  it('renders core information', () => {
    render(<RecommendationCard item={mockItem} rank={1} theme="books" />)
    expect(screen.getByText('沙丘')).toBeInTheDocument()
    expect(screen.getByText(/由 弗兰克·赫伯特/)).toBeInTheDocument()
  })

  it('shows metadata pills', () => {
    render(<RecommendationCard item={mockItem} rank={2} theme="books" />)
    expect(screen.getByText('年份')).toBeInTheDocument()
    expect(screen.getByText('1965')).toBeInTheDocument()
  })

  it('displays summary and reason', () => {
    render(<RecommendationCard item={mockItem} rank={3} theme="books" />)
    expect(screen.getByText(mockItem.summary)).toBeInTheDocument()
    expect(screen.getByText(mockItem.reason)).toBeInTheDocument()
  })

  it('shows rank badge', () => {
    render(<RecommendationCard item={mockItem} rank={3} theme="books" />)
    expect(screen.getByText('#3')).toBeInTheDocument()
  })
})
