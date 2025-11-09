import { ThemeProvider } from '../../shared/ThemeProvider'
import { SharedFeedPage } from '../../shared/pages/FeedPage'
import { iteration2Theme } from '../themeAdapter'

export function FeedPageV2() {
  return (
    <ThemeProvider theme={iteration2Theme}>
      <SharedFeedPage />
    </ThemeProvider>
  )
}














