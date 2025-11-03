import { ThemeProvider } from '../../shared/ThemeProvider'
import { SharedGraphLabPage } from '../../shared/pages/GraphLabPage'
import { iteration1Theme } from '../themeAdapter'

export function GraphLabPageV1() {
  return (
    <ThemeProvider theme={iteration1Theme}>
      <SharedGraphLabPage />
    </ThemeProvider>
  )
}

