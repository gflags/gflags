/* Copyright (c) 2009, Google Inc.
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 * 
 *     * Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above
 * copyright notice, this list of conditions and the following disclaimer
 * in the documentation and/or other materials provided with the
 * distribution.
 *     * Neither the name of Google Inc. nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ---
 * Author: Craig Silverstein
 */

#ifndef _WIN32
# error You should only be including windows/port.cc in a windows environment!
#endif

#include <config.h>
#include <string.h>    // for strlen(), memset(), memcmp()
#include <stdlib.h>    // for _putenv, etc.
#include <assert.h>
#include <stdarg.h>    // for va_list, va_start, va_end
#include <windows.h>
#include "port.h"

// These call the windows _vsnprintf, but always NUL-terminate.
#if !defined(__MINGW32__) && !defined(__MINGW64__)  /* mingw already defines */
int safe_vsnprintf(char *str, size_t size, const char *format, va_list ap) {
  if (size == 0)        // not even room for a \0?
    return -1;          // not what C99 says to do, but what windows does
  str[size-1] = '\0';
  return _vsnprintf(str, size-1, format, ap);
}

int snprintf(char *str, size_t size, const char *format, ...) {
  int r;
  va_list ap;
  va_start(ap, format);
  r = vsnprintf(str, size, format, ap);
  va_end(ap);
  return r;
}
#endif  /* #if !defined(__MINGW32__) && !defined(__MINGW64__) */

void setenv(const char* name, const char* value, int) {
  // In windows, it's impossible to set a variable to the empty string.
  // We handle this by setting it to "0" and the NUL-ing out the \0.
  // That is, we putenv("FOO=0") and then find out where in memory the
  // putenv wrote "FOO=0", and change it in-place to "FOO=\0".
  // c.f. http://svn.apache.org/viewvc/stdcxx/trunk/tests/src/environ.cpp?r1=611451&r2=637508&pathrev=637508
  static const char* const kFakeZero = "0";
  if (*value == '\0')
    value = kFakeZero;
  // Apparently the semantics of putenv() is that the input
  // must live forever, so we leak memory here. :-(
  const int nameval_len = strlen(name) + 1 + strlen(value) + 1;
  char* nameval = reinterpret_cast<char*>(malloc(nameval_len));
  snprintf(nameval, nameval_len, "%s=%s", name, value);
  _putenv(nameval);
  if (value == kFakeZero) {
    nameval[nameval_len - 2] = '\0';   // works when putenv() makes no copy
    if (*getenv(name) != '\0')
      *getenv(name) = '\0';            // works when putenv() copies nameval
  }
}
