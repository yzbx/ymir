import { forwardRef, useEffect, useImperativeHandle } from "react"
import { message, Tag } from "antd"

import t from "@/utils/t"
import confirm from '@/components/common/dangerConfirm'
import useFetch from '@/hooks/useFetch'

import VersionName from '@/components/result/VersionName'

const Hide = forwardRef(({ type = 0, msg = 'dataset.action.hide.confirm.content',
  excludeMsg = 'dataset.action.hide.confirm.exclude', ok = () => { }}, ref) => {
  const [hideResult, remoteHide] = useFetch(`${!type ? 'dataset' : 'model'}/hide`)

  useEffect(() => hideResult && ok(hideResult), [hideResult])

  useImperativeHandle(ref, () => {
    return {
      hide,
    }
  })

  function hide(versions, exclude = []) {
    if (!versions?.length) {
      return message.warn(t('common.selected.required'))
    }
    const hideVersions = versions.filter(vs => !exclude.includes(vs.id))
    const labels = getLabels(hideVersions)
    const excludeLabels = getLabels(versions.filter(vs => exclude.includes(vs.id)))
    const ids = hideVersions.map(({ id }) => id)
    const pid = versions[0].projectId
    const emsg = <div style={{ color: 'red' }}>{t(excludeMsg, { labels: excludeLabels })}</div>
    if (!hideVersions?.length) {
      return message.error(emsg)
    }
    confirm({
      content: <div>
        <p>{t(msg, { name: labels })} </p>
        {excludeLabels.length ? emsg : null}
      </div>,
      onOk: () => remoteHide({ pid, ids }),
      okText: t('common.action.hide'),
    })
  }

  return null
})

const getLabels = (labels) => labels.map(version => <Tag
  style={{ margin: '0 5px', display: 'inline-block' }}
  key={version.id}>
  <VersionName result={version} />
</Tag>)

export default Hide
