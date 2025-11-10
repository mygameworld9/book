export const THEME_CONFIG = {
  books: {
    label: '书籍',
    icon: '📚',
    description: '用多维画像匹配最懂你的阅读灵感',
    placeholder: '描述你想读的书或最近的阅读心情……',
    examples: [
      '我想读扩展想象力的硬核科幻',
      '推荐2本轻松治愈的现代文学',
    ],
    accent: '#6c63ff',
  },
  games: {
    label: '游戏',
    icon: '🎮',
    description: '按平台、机制与心流状态精准匹配下一款游戏',
    placeholder: '说说你喜欢的玩法、平台或想体验的节奏……',
    examples: [
      '最近想玩剧情深度的动作游戏',
      '推荐 Switch 上适合和朋友合作的游戏',
    ],
    accent: '#ff7a18',
  },
  movies: {
    label: '电影',
    icon: '🎬',
    description: '结合观影场景与情绪诉求输出精选片单',
    placeholder: '告诉我你想看的电影类型、情绪或导演……',
    examples: [
      '推荐几部适合独自观看的烧脑电影',
      '想找适合家庭观影的温馨影片',
    ],
    accent: '#00b894',
  },
  anime: {
    label: '动漫',
    icon: '🧩',
    description: '按世界观、设定与情感体验打造动漫歌单',
    placeholder: '描述你想看的动漫风格或情绪……',
    examples: [
      '想看充满热血冒险的少年漫',
      '推荐静心放松的治愈系动画',
    ],
    accent: '#ff5e7e',
  },
}

export const THEME_ORDER = Object.keys(THEME_CONFIG)
