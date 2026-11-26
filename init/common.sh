#!/bin/sh

# 命令传递
apply_handle() {
  if [ -n "$1" ]; then
    if [ "$3" == "new" ]; then
      eval "$1"
      return
    fi
    echo "$2" | eval "$1"
    return
  fi
  echo $2
}

# Telegram MarkdownV2 特殊字符转义
tg_escape() {
  local input="$1"
  local char
  local result=""
  while IFS= read -r -n1 char || [[ -n "$char" ]]; do
    case "$char" in
      '\'| '_'|'*'|'['|']'|'('|')'|'~'|'`'|'>'|'#'|'+'|'-'|'='|'|'|'{'|'}'|'.'|'!')
        result+="\\$char"
        ;;
      *)
        result+="$char"
        ;;
    esac
  done <<< "$input"
  printf '%s' "${result%$'\n'}"
}

# 获取最新版本函数
get_latest_version() {
    case "$1" in
      release)
        # 使用 Releases API（按时间排序）
        github_api_request "https://api.github.com/repos/$2/releases/latest" GET | jq -r '.tag_name'
        ;;
      tag)
        # 获取按时间排序的最新 Tag（需 GitHub API v3）
        github_api_request "https://api.github.com/repos/$2/tags" GET | jq -r '.[0].name'
        ;;
      *)
        exit 1
        ;;
    esac
}

send_telegram_message() {
  local response http_code
  response=$(mktemp)
  http_code=$(curl -sS \
    -X POST \
    --url "https://api.telegram.org/bot$1/sendMessage" \
    --header 'Content-Type: application/json' \
    --data "$2" \
    -o "$response" \
    -w '%{http_code}') || {
      local ret=$?
      cat "$response" >&2
      rm -f "$response"
      return "$ret"
    }
  if (( http_code < 200 || http_code >= 300 )); then
    echo "Telegram 请求失败，HTTP 状态码: $http_code 请求体：$2" >&2
    cat "$response" >&2
    rm -f "$response"
    return 1
  fi
  rm -f "$response"
}

github_api_error_message_tg_send() {
  printf -v textData '[%s][◯ 请求GitHubAPI成功]\n报文: \n`%s`' \
  "$project_program" \
  "$1"
  reqData=$(jq -cn \
    --arg chatId "$chatId" \
    --arg textData "$textData" \
    '{
        chat_id: $chatId,
        text: $textData
    }')
    send_telegram_message $tgContentBotKey "$reqData"
}

github_api_success_message_tg_send() {
  printf -v textData '[%s][◯ 请求GitHubAPI成功]\n报文: \n`%s`' \
  "$project_program" \
  "$1"
  reqData=$(jq -cn \
    --arg chatId "$chatId" \
    --arg textData "$textData" \
    '{
        chat_id: $chatId,
        text: $textData
    }')
    send_telegram_message $tgContentBotKey "$reqData"
}

# GitHub API 请求
github_api_request() {
  local url="$1"
  local method="${2:-GET}"
  local data="$3"
  local body headers http_code
  local retry_after reset_time remaining wait_time
  local retries=0
  local max_retries=5
  local response_body
  local response_headers
  while (( retries <= max_retries )); do
    headers=$(mktemp) || return 1
    body=$(mktemp) || {
      rm -f "$headers"
      return 1
    }
    local -a curl_args=(
      -sSL
      -D "$headers"
      -o "$body"
      -w '%{http_code}'
      --connect-timeout 10
      --max-time 30
      -X "$method"
      -H "Authorization: Bearer ${GITHUB_TOKEN}"
      -H "Accept: application/vnd.github+json"
      -H "X-GitHub-Api-Version: 2022-11-28"
    )
    if [[ -n "$data" ]]; then
      curl_args+=(
        -H "Content-Type: application/json"
        --data "$data"
      )
    fi
    http_code=$(curl "${curl_args[@]}" "$url")
    if [[ $? -ne 0 ]]; then
      echo "GitHub API: 网络请求失败" >&2
      github_api_error_message_tg_send "网络请求失败"
      rm -f "$headers" "$body"
      return 1
    fi
    response_body=$(cat "$body")
    response_headers=$(cat "$headers")
    case "$http_code" in
      200|201|202|204)
        cat "$body"
        local success_text="请求头: $response_headers, 响应体: $response_body"
        if ((${#success_text} > 3000)); then
          success_text="${success_text:0:3000}... 内容已截断"
        fi
        github_api_success_message_tg_send "$success_text"
        rm -f "$headers" "$body"
        return 0
        ;;
      403|429)
        remaining=$(awk 'BEGIN{IGNORECASE=1} /^X-RateLimit-Remaining:/ {gsub("\r",""); print $2}' "$headers")
        retry_after=$(awk 'BEGIN{IGNORECASE=1} /^Retry-After:/ {gsub("\r",""); print $2}' "$headers")
        reset_time=$(awk 'BEGIN{IGNORECASE=1} /^X-RateLimit-Reset:/ {gsub("\r",""); print $2}' "$headers")
        if [[ -n "$retry_after" ]]; then
          wait_time="$retry_after"
        elif [[ "$remaining" == "0" && -n "$reset_time" ]]; then
          wait_time=$((reset_time - $(date +%s)))
        else
          cat "$body"
          rm -f "$headers" "$body"
          return 0
        fi
        (( wait_time < 1 )) && wait_time=1
        rm -f "$headers" "$body"
        if (( retries >= max_retries )); then
          echo "GitHub API: 超过最大重试次数" >&2
          github_api_error_message_tg_send "超过最大重试次数 响应头: $response_headers, 响应体: $response_body"
          return 1
        fi
        echo "GitHub API: 限流，等待 ${wait_time}s 后重试" >&2
        github_api_error_message_tg_send "限流，等待 ${wait_time}s 后重试 响应头: $response_headers, 响应体: $response_body"
        sleep "$wait_time"
        ((retries++))
        ;;
      401)
        echo "GitHub API: Token 无效或已过期" >&2
        cat "$body" >&2
        github_api_error_message_tg_send "Token 无效或已过期 响应体: $response_body"
        rm -f "$headers" "$body"
        return 1
        ;;
      404)
        echo "GitHub API: 仓库或资源不存在" >&2
        cat "$body" >&2
        github_api_error_message_tg_send "仓库或资源不存在 响应体: $response_body"
        rm -f "$headers" "$body"
        return 1
        ;;
      5??)
        echo "GitHub API: 服务端错误 (HTTP $http_code)" >&2
        cat "$body" >&2
        github_api_error_message_tg_send "服务端错误 (HTTP $http_code) 响应体: $response_body"
        rm -f "$headers" "$body"
        return 1
        ;;
      *)
        echo "GitHub API: 请求失败 (HTTP $http_code)" >&2
        cat "$body" >&2
        github_api_error_message_tg_send "请求失败 (HTTP $http_code) 响应体: $response_body"
        rm -f "$headers" "$body"
        return 1
        ;;
    esac
  done
}
