import { ThemeProvider } from '../../shared/ThemeProvider'
import { SharedGraphLabPage } from '../../shared/pages/GraphLabPage'
import { iteration3Theme } from '../themeAdapter'

export function GraphLabPageV3() {
  return (
    <ThemeProvider theme={iteration3Theme}>
      <SharedGraphLabPage />
    </ThemeProvider>
  )
}














