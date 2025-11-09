import { ThemeProvider } from '../../shared/ThemeProvider'
import { SharedFeedPage } from '../../shared/pages/FeedPage'
import { iteration3Theme } from '../themeAdapter'

export function FeedPageV3() {
  return (
    <ThemeProvider theme={iteration3Theme}>
      <SharedFeedPage />
    </ThemeProvider>
  )
}












