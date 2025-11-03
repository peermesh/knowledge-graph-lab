import { ThemeProvider } from '../../shared/ThemeProvider'
import { SharedFeedPage } from '../../shared/pages/FeedPage'
import { iteration1Theme } from '../themeAdapter'

export function FeedPageV1() {
  return (
    <ThemeProvider theme={iteration1Theme}>
      <SharedFeedPage />
    </ThemeProvider>
  )
}
